from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import empty

from .. import models


class ValidationError(serializers.ValidationError):
    pass


class FieldSerializer(serializers.ModelSerializer):
    """
    serializer for Field model read and update.
    """

    id = serializers.IntegerField(required=False)

    class Meta:
        model = models.FieldName
        exclude = (
            "risk_model",
            "deleted",
            "created_on",
            "updated_on",
        )  # add slug here to remove from web app
        read_only_fields = ("slug",)

    def validate(self, data):
        """
        Checks that min_length is <= max_length.
        Checks that select & multiselect fields have an array in choices field.
        """
        # Checks that min_length is <= max_length.
        if (
            "min_length" in data
            and "max_length" in data
            and data["min_length"]
            and data["max_length"]
            and data["min_length"] > data["max_length"]
        ):
            raise serializers.ValidationError(
                {
                    "min_length": [
                        "Min Length can't be greater than Max Length."
                    ]
                }
            )

        # check that select & multiselect fields has an array in choices field
        if data["field_type"] in ["select", "multiselect"] and (
            "choices" not in data
            or data["choices"] is None
            or (
                isinstance(data["choices"], list) and len(data["choices"]) == 0
            )
        ):
            raise serializers.ValidationError(
                {"choices": ["Choices are required for this Field type."]}
            )

        # check that regex field type has 'regex_pattern' set
        if data["field_type"] == "regex" and (
            "regex_pattern" not in data or data["regex_pattern"] is None
        ):
            raise serializers.ValidationError(
                {
                    "regex_pattern": [
                        "Regex Pattern is required for the REGEX Field type."
                    ]
                }
            )
        return data


class RiskModelSerializer(serializers.ModelSerializer):
    """
    serializer for Risk Model
    """

    fields = FieldSerializer(many=True)

    class Meta:
        model = models.RiskModel
        fields = (
            "id",
            "name",
            "button",
            "description",
            "success_msg",
            "activated",
            "fields",
        )

    def validate_fields(self, value):
        """
        Check that the 'order' of fields have an incremental sequence
        Check that the 'name' of fields are unique
        """
        # check number of fields
        if len(value) == 0:
            raise serializers.ValidationError(
                "Risk Model has no fields. At least one field is required."
            )
        # check the fields order sequence
        fields_order_values = [d["order"] for d in value]
        if (
            fields_order_values[0] != 1
            or not fields_order_values[len(fields_order_values) - 1]
            - fields_order_values[0]
            == len(fields_order_values) - 1
        ):
            raise serializers.ValidationError(
                "Riskmodel fields must have a sequential order."
            )
        # check field name uniqueness
        fields_name_values = [d["name"] for d in value]
        if len(fields_name_values) != len(set(fields_name_values)):
            raise serializers.ValidationError(
                "Riskmodel fields must have unique names."
            )
        return value

    def create(self, validated_data):
        """
        Handles POST requests to riskmodel endpoint
        """
        self.new_fields = validated_data.pop("fields")
        self.instance = super().create(validated_data)

        # delete id key of the fields, just incase its mistakenly added to the
        # client
        for field_data in self.new_fields:
            field_data.pop("id", None)

        self.create_fields()
        return self.instance

    def update(self, instance, validated_data):
        """
        Handles PUT requests to riskmodel endpoint
        by updating RiskModel instance and creating, updating or deleting
        FieldName instances
        """
        fields_data = validated_data.pop("fields")

        # update riskmodel, without 'fields' field
        super().update(instance, validated_data)

        self.update_fields(fields_data)
        self.delete_fields()
        self.create_fields()

        return instance

    def update_fields(self, fields_data):
        """
        update fields that exist in db with data
        """
        self.new_fields = []
        self.updated_fields_id = []
        for field_data in fields_data:
            field_id = field_data.get("id", None)
            if field_id:
                # update
                field = get_object_or_404(models.FieldName, id=field_id)
                update_field_serializer = FieldSerializer(
                    instance=field, data=field_data
                )
                update_field_serializer.is_valid(raise_exception=True)
                update_field_serializer.save()
                self.updated_fields_id.append(field.id)
            else:
                # create: append to bulk list
                self.new_fields.append(field_data)

    def delete_fields(self):
        """
        Soft Deletes fields in db that were not re-posted
        """
        delete_queryset = self.instance.fields.all().exclude(
            id__in=self.updated_fields_id
        )
        for x in delete_queryset:
            x.deleted = True
            x.save()

    def create_fields(self):
        """
        Create fields in db that were not existing before
        """
        create_field_serializer = FieldSerializer(
            data=self.new_fields, many=True
        )
        create_field_serializer.is_valid(raise_exception=True)
        create_field_serializer.save(risk_model_id=self.instance.id)

    def to_representation(self, instance):
        """
        list nested fields in ascending order of 'order' attribute
        """
        response = super().to_representation(instance)
        response["fields"] = sorted(
            response["fields"], key=lambda x: x["order"]
        )
        return response


class FieldValueSerializer(serializers.ModelSerializer):
    """
    Input serializer for form field values
    """

    class Meta:
        model = models.FieldValue
        fields = "__all__"

    def __init__(self, instance=None, data=empty, **kwargs):
        # Instantiate the superclass normally
        super(FieldValueSerializer, self).__init__(data=data, **kwargs)
        field = kwargs["context"].pop("field", None)
        self.invalid_field_errors = {}

        if field.field_type in ["text", "textarea", "password"]:
            self.fields["value"] = serializers.CharField(
                max_length=field.max_length,
                min_length=field.min_length,
                allow_null=not field.required,
            )
        elif field.field_type == "email":
            self.fields["value"] = serializers.EmailField(
                max_length=field.max_length,
                min_length=field.min_length,
                allow_null=not field.required,
            )
        elif field.field_type == "float":
            self.fields["value"] = serializers.FloatField(
                allow_null=not field.required
            )
        elif field.field_type == "number":
            self.fields["value"] = serializers.IntegerField(
                allow_null=not field.required, max_value=None, min_value=None
            )  # add min and max
        elif field.field_type == "date":
            self.fields["value"] = serializers.DateField(
                allow_null=not field.required
            )
        elif field.field_type == "time":
            self.fields["value"] = serializers.TimeField(
                allow_null=not field.required
            )
        elif field.field_type in ["select", "radio"]:
            self.fields["value"] = serializers.ChoiceField(
                allow_null=not field.required, choices=field.choices
            )
        elif field.field_type == "multiselect":
            self.fields["value"] = serializers.MultipleChoiceField(
                allow_null=not field.required, choices=field.choices
            )
        elif field.field_type in ["checkbox", "switch"]:
            self.fields["value"] = serializers.BooleanField()
        elif field.field_type == "url":
            self.fields["value"] = serializers.URLField(
                max_length=field.max_length,
                min_length=field.min_length,
                allow_null=not field.required,
            )
        elif field.field_type == "array":
            self.fields["value"] = serializers.ListField(
                allow_null=not field.required
            )  # add minlen and max
        elif field.field_type == "regex":
            self.fields["value"] = serializers.RegexField(
                field.regex_pattern,
                max_length=field.max_length,
                min_length=field.min_length,
                allow_null=not field.required,
            )
        elif field.field_type == "file":
            self.fields["value"] = serializers.FileField(
                allow_null=not field.required
            )
        else:
            self.invalid_field_errors = {
                "fields": [f"{field.field_type} is not a valid field type."]
            }

    def validate(self, data):
        """
        validates the uniqueness of the field's value for unique fields
        """
        if (
            data["field"].unique
            and models.FieldValue.objects.filter(
                field=data["field"],
                value=data["value"],
                form_submit__success=True,
            ).exists()
        ):
            raise ValidationError(
                {
                    data["field"].name: [
                        "An entry with this value already exists."
                    ]
                }
            )
        return data

    def is_valid(self, raise_exception=False):
        """
        additionally checks if the instance variable invalid_field_errors
        contain errors.
        """
        is_valid = super().is_valid(raise_exception)
        if self.invalid_field_errors:
            self._errors = self.invalid_field_errors
            is_valid = not bool(self._errors)
        return is_valid


class FieldValueResponseSerializer(serializers.ModelSerializer):
    """
    Output/Response serializer for form field values
    """

    field_name = serializers.CharField(source="field.name")
    field_type = serializers.CharField(source="field.field_type")
    value = serializers.SerializerMethodField()

    class Meta:
        model = models.FieldValue
        exclude = ("form_submit", "field", "created_on", "updated_on")

    def get_value(self, obj):
        if obj.field.field_type == "file":
            if (
                settings.DEFAULT_FILE_STORAGE
                != "django.core.files.storage.FileSystemStorage"
            ):
                return f"{settings.STATIC_URL}{obj.value}"
            else:
                protocol = (
                    "https://"
                    if self.context["request"].is_secure()
                    else "http://"
                )
                host = self.context["request"].META["HTTP_HOST"]
                return f"{protocol}{host}{obj.value}"
        return obj.value


class RiskDataSerializer(serializers.Serializer):
    """
    Handles Risk Form Data
    """

    risk_model = serializers.IntegerField()
    risk_model_name = serializers.CharField(
        max_length=255
    )  # remove this: not needed
    data = serializers.DictField()

    def validate(self, data):
        """
        Custom validation that confirms all required fields are in data json
        """
        fields = models.RiskModel.objects.get(
            id=data["risk_model"]
        ).fields.all()
        for field in fields:
            if field.required and field.slug not in data["data"]:
                raise serializers.ValidationError(
                    {"data": [f"{field.name} is required."]}
                )
        return data


class RiskDataLogSerializer(serializers.ModelSerializer):
    """
    serializer for FormSubmit Model
    """

    class Meta:
        model = models.FormSubmit
        fields = "__all__"
