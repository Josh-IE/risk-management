from django.http import QueryDict
from django.shortcuts import get_object_or_404

from .. import models
from ..v1 import serializers
from . import utils


class RiskDataProcessor:
    """
    Class that helps with processing risk data create logic
    """

    def __init__(self, data):
        """
        instantiate class with request data
        """
        self.data = data

    def querydict_to_dict(self):
        """
        transforms request data to dict if it's a QueryDict
        """
        if isinstance(self.data, QueryDict):
            # Querydict is used if its a multipart data
            return utils.nested_field_parse(self.data)
        return self.data

    def build_field_value_object(self, field, value, form_submit):
        """
        builds and returns a FieldValue dict
        """
        value = None if value == "" else value
        if field.field_type in ["checkbox", "switch"] and value is None:
            value = False
        field_value_data = {
            "form_submit": form_submit.pk,
            "field": field.pk,
            "value": value,
        }
        return field_value_data

    def create_fields_data(self):
        """
        validate and create risk form field data
        """
        # Log form submission event
        form_submit = models.FormSubmit.objects.create(
            risk_model_id=self.validated_data["risk_model"]
        )
        # loop through the individual field-value pairs in the 'data' nested
        # dict, validate and append to list for efficient bulk create
        bulk_field_value_ls = []
        for field, value in self.validated_data["data"].items():
            field = get_object_or_404(models.FieldName, slug=field)
            field_value_data = self.build_field_value_object(
                field, value, form_submit
            )
            context = {"field": field}
            field_value_serializer = serializers.FieldValueSerializer(
                data=field_value_data, context=context
            )
            if field_value_serializer.is_valid():
                # if field type is file and validation is successful,
                # store file, then update field with file url
                if field.field_type == "file":
                    field_value_serializer.validated_data[
                        "value"
                    ] = utils.store_file(value)
                bulk_field_value_ls.append(
                    models.FieldValue(**field_value_serializer.validated_data)
                )
            else:
                error_dict = field_value_serializer.errors
                if "value" in error_dict:
                    # rename the 'value' key to that of the field name
                    error_dict[field.name] = error_dict.pop("value")
                    raise serializers.ValidationError(error_dict)
                else:
                    raise serializers.ValidationError(error_dict)
        # bulk save form data
        models.FieldValue.objects.bulk_create(bulk_field_value_ls)
        form_submit.success = True
        form_submit.save()
        data = {
            "form_submit": form_submit.pk,
            "risk_model": self.validated_data["risk_model"],
            "risk_model_name": self.validated_data["risk_model_name"],
            "time_created": form_submit.created_on,
        }
        return data
