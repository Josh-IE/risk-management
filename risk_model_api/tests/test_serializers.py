from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from .. import models
from ..utils import utils
from ..v1 import serializers


class FieldSerializerTestCase(TestCase):
    """
    Unit tests for the Field serializer.
    """

    def setUp(self):
        client = models.Client.objects.create(name="Client 1")
        self.risk_model = models.RiskModel.objects.create(
            client=client, name="Risk Model 1", button="Save"
        )
        models.FieldName.objects.create(
            name="Field 1",
            field_type="text",
            risk_model=self.risk_model,
            order=1,
        )
        models.FieldName.objects.create(
            name="Field 2",
            field_type="text",
            risk_model=self.risk_model,
            order=2,
            deleted=True,
        )

    def test_choices_in_select_field_type(self):
        """
        'select' field type must have choices.
        """
        data = {
            "name": "Framework",
            "field_type": "select",
            "default": "Vue",
            "choices": None,
            "required": True,
            "help_text": "What frontend framework do you use",
            "order": 1,
        }
        serializer = serializers.FieldSerializer(data=data)
        assert False is serializer.is_valid()
        self.assertIn("choices", serializer.errors)
        msg = "Choices are required for this Field type."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_valid_choices_in_select_field_type(self):
        """
        'select' field type must have valid choices.
        """
        data = {
            "name": "Framework",
            "field_type": "select",
            "default": "Vue",
            "choices": "Vue, React, Angular",
            "required": True,
            "help_text": "What frontend framework do you use",
            "order": 1,
        }
        serializer = serializers.FieldSerializer(data=data)
        assert False is serializer.is_valid()
        self.assertIn("choices", serializer.errors)
        msg = 'Expected a list of items but got type "str".'
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_choices_in_multiselect_field_type(self):
        """
        'multiselect' field type must have valid choices.
        """
        data = {
            "name": "Framework",
            "field_type": "multiselect",
            "default": "Vue",
            "choices": [],
            "required": True,
            "help_text": "What frontend framework do you use",
            "order": 1,
        }
        serializer = serializers.FieldSerializer(data=data)
        assert False is serializer.is_valid()
        self.assertIn("choices", serializer.errors)
        msg = "Choices are required for this Field type."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_regex_pattern_in_regex_field_type(self):
        """
        'regex' field type must have a 'regex_pattern'.
        """
        data = {
            "name": "Registration Code",
            "field_type": "regex",
            "required": True,
            "help_text": "Provide your registration code",
            "order": 1,
        }
        serializer = serializers.FieldSerializer(data=data)
        assert False is serializer.is_valid()
        self.assertIn("regex_pattern", serializer.errors)
        msg = "Regex Pattern is required for the REGEX Field type."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_invalid_min_length(self):
        """
        Validation error is raised if min_length > settings.FIELD_MAX_LENGTH.
        """
        data = {
            "name": "Name",
            "field_type": "text",
            "default": "John",
            "min_length": settings.FIELD_MAX_LENGTH + 1,
            "choices": None,
            "required": True,
            "help_text": "What is your name?",
            "order": 1,
        }
        serializer = serializers.FieldSerializer(data=data)
        assert False is serializer.is_valid()
        self.assertIn("min_length", serializer.errors)
        max_length = settings.FIELD_MAX_LENGTH
        msg = f"Ensure this value is less than or equal to {max_length}."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_valid_min_length(self):
        """
        Serializer is valid when min_length <= settings.FIELD_MAX_LENGTH.
        """
        data = {
            "name": "Name",
            "field_type": "text",
            "default": "John",
            "min_length": settings.FIELD_MAX_LENGTH,
            "choices": None,
            "required": True,
            "help_text": "What is your name?",
            "order": 1,
        }
        serializer = serializers.FieldSerializer(data=data)
        assert True is serializer.is_valid()

    def test_invalid_max_length(self):
        """
        Validation error is raised if max_length > settings.FIELD_MAX_LENGTH.
        """
        data = {
            "name": "Name",
            "field_type": "text",
            "default": "John",
            "max_length": settings.FIELD_MAX_LENGTH + 1,
            "choices": None,
            "required": True,
            "help_text": "What is your name?",
            "order": 1,
        }
        serializer = serializers.FieldSerializer(data=data)
        assert False is serializer.is_valid()
        self.assertIn("max_length", serializer.errors)
        max_length = settings.FIELD_MAX_LENGTH
        msg = f"Ensure this value is less than or equal to {max_length}."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_valid_max_length(self):
        """
        Serializer is valid when max_length <= settings.FIELD_MAX_LENGTH.
        """
        data = {
            "name": "Name",
            "field_type": "text",
            "default": "John",
            "max_length": settings.FIELD_MAX_LENGTH,
            "choices": None,
            "required": True,
            "help_text": "What is your name?",
            "order": 1,
        }
        serializer = serializers.FieldSerializer(data=data)
        assert True is serializer.is_valid()

    def test_min_length_max_length(self):
        """
        Validation error is raised if min_length > max_length.
        """
        data = {
            "name": "Name",
            "field_type": "text",
            "default": "John",
            "min_length": 5,
            "max_length": 4,
            "choices": None,
            "required": True,
            "help_text": "What is your name?",
            "order": 1,
        }
        serializer = serializers.FieldSerializer(data=data)
        assert False is serializer.is_valid()
        self.assertIn("min_length", serializer.errors)
        msg = "Min Length can't be greater than Max Length."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_invalid_field_type(self):
        """
        Invalid field_type raises validation error.
        """
        data = {
            "name": "Name",
            "field_type": "texter",
            "default": "John",
            "min_length": 4,
            "max_length": 10,
            "choices": None,
            "required": True,
            "help_text": "What is your name?",
            "order": 1,
        }
        serializer = serializers.FieldSerializer(data=data)
        assert False is serializer.is_valid()
        self.assertIn("field_type", serializer.errors)
        msg = '"texter" is not a valid choice.'
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)


class RiskModelSerializerTestCase(TestCase):
    """
    Unit tests for the RiskModel serializer.
    """

    def test_reversed_fields_order(self):
        """
        The order of the risk model fields must follow an incremental sequence.
        """
        field_data = [
            {
                "name": "Location",
                "field_type": "text",
                "default": "World Wide",
                "min_length": 5,
                "max_length": 10,
                "choices": None,
                "required": True,
                "help_text": "Where are you located?",
                "order": 2,
            },
            {
                "name": "Occupation",
                "field_type": "text",
                "default": "Engineer",
                "min_length": 5,
                "max_length": 10,
                "choices": None,
                "required": True,
                "help_text": "What do you do for a living?",
                "order": 1,
            },
        ]
        data = {
            "name": "Auto Insurance",
            "button": "Create",
            "activated": True,
            "fields": field_data,
        }
        serializer = serializers.RiskModelSerializer(data=data)
        assert False is serializer.is_valid()
        self.assertIn("fields", serializer.errors)
        msg = "Riskmodel fields must have a sequential order."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_non_unique_field_names(self):
        """
        Field names of a riskmodel must be unique.
        """
        field_data = [
            {
                "name": "Location",
                "field_type": "text",
                "default": "World Wide",
                "min_length": 5,
                "max_length": 10,
                "choices": None,
                "required": True,
                "help_text": "Residential location?",
                "order": 1,
            },
            {
                "name": "Location",
                "field_type": "text",
                "default": "California",
                "min_length": 5,
                "max_length": 10,
                "choices": None,
                "required": True,
                "help_text": "Office Location?",
                "order": 2,
            },
        ]
        data = {
            "name": "Auto Insurance",
            "button": "Create",
            "activated": True,
            "fields": field_data,
        }
        serializer = serializers.RiskModelSerializer(data=data)
        assert False is serializer.is_valid()
        self.assertIn("fields", serializer.errors)
        msg = "Riskmodel fields must have unique names."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)


class RiskDataSerializerTestCase(TestCase):
    """
    Unit tests for the RiskData serializer
    """

    def setUp(self):
        # create client
        client = models.Client.objects.create(name="Client 1")

        # create risk model
        self.risk_model = models.RiskModel.objects.create(
            client=client, name="Risk Model 1", button="Save"
        )
        # create fields
        self.normal_field_1 = models.FieldName.objects.create(
            name="First Name",
            field_type="text",
            risk_model=self.risk_model,
            order=1,
        )
        self.normal_field_2 = models.FieldName.objects.create(
            name="Email",
            field_type="email",
            risk_model=self.risk_model,
            order=2,
        )
        self.normal_field_3 = models.FieldName.objects.create(
            name="Age",
            field_type="number",
            risk_model=self.risk_model,
            order=3,
        )

    def test_missing_required_risk_data_fields(self):
        """
        The absence of required field(s) in data raises a validation error.
        """
        risk_data = {
            "risk_model": self.risk_model.id,
            "risk_model_name": self.risk_model.name,
            "data": {
                self.normal_field_1.slug: "Joshua",
                self.normal_field_2.slug: "josh@techintel.dev",
            },
        }
        serializer = serializers.RiskDataSerializer(data=risk_data)
        assert False is serializer.is_valid()
        self.assertIn("data", serializer.errors)
        msg = "Age is required."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)


class FieldValueSerializerTestCase(TestCase):
    """
    Unit tests for the FieldValue serializer.
    """

    def setUp(self):
        # create client
        client = models.Client.objects.create(name="Client 1")

        # create risk model
        self.risk_model = models.RiskModel.objects.create(
            client=client, name="Risk Model 1", button="Save"
        )

    def test_repeat_data_in_unique_field(self):
        """
        Validation error is raised if repeated data is passed to unique field
        """
        repeated_data = "California"
        # setup unique field
        field = models.FieldName.objects.create(
            name="State of Residence",
            field_type="text",
            risk_model=self.risk_model,
            order=1,
            unique=True,
        )
        # initial form submission
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        # create data submission with repeated data
        models.FieldValue.objects.create(
            form_submit=form_submit, field=field, value=repeated_data
        )

        # setup repeated data for serialization
        field_value_data = {
            "form_submit": form_submit.id,
            "field": field.id,
            "value": repeated_data,
        }
        context = {"field": field}
        serializer = serializers.FieldValueSerializer(
            data=field_value_data, context=context
        )
        assert False is serializer.is_valid()
        self.assertIn(field.name, serializer.errors)
        msg = "An entry with this value already exists."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_repeat_data_in_unique_field_behavior(self):
        """
        Repeated data is valid if previous data form submission failed.
        """
        repeated_data = "California"
        # setup unique field
        field = models.FieldName.objects.create(
            name="State of Residence",
            field_type="text",
            risk_model=self.risk_model,
            order=1,
            unique=True,
        )
        # initail form submission failed
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=False
        )
        # create data submission with repeated data
        models.FieldValue.objects.create(
            form_submit=form_submit, field=field, value=repeated_data
        )

        # setup repeated data for serialization
        field_value_data = {
            "form_submit": form_submit.id,
            "field": field.id,
            "value": repeated_data,
        }
        context = {"field": field}
        serializer = serializers.FieldValueSerializer(
            data=field_value_data, context=context
        )
        assert True is serializer.is_valid()
        self.assertEqual(serializer.validated_data["value"], repeated_data)

    def test_risk_data_invalid_field_type(self):
        """
        Submitting data against invalid field type raises validation error.
        """
        field = models.FieldName.objects.create(
            name="Agreement Document",
            field_type="pdf",
            risk_model=self.risk_model,
            order=1,
        )
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        field_value_data = {
            "form_submit": form_submit.id,
            "field": field.id,
            "value": "agreement-doc.pdf",
        }

        serializer = serializers.FieldValueSerializer(
            data=field_value_data, context={"field": field}
        )
        assert False is serializer.is_valid()
        self.assertIn("fields", serializer.errors)
        msg = "pdf is not a valid field type."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_to_date_field_type(self):
        """
        Invalid date data on a date field raises validation error.
        """
        field = models.FieldName.objects.create(
            name="Date of Expiry",
            field_type="date",
            risk_model=self.risk_model,
            order=1,
        )
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        field_value_data = {
            "form_submit": form_submit.id,
            "field": field.id,
            "value": "April272006",
        }

        serializer = serializers.FieldValueSerializer(
            data=field_value_data, context={"field": field}
        )
        assert False is serializer.is_valid()
        msg = "Date has wrong format."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_to_float_field_type(self):
        """
        Invalid float data on a float field raises validation error.
        """
        field = models.FieldName.objects.create(
            name="Amount",
            field_type="float",
            risk_model=self.risk_model,
            order=1,
        )
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        field_value_data = {
            "form_submit": form_submit.id,
            "field": field.id,
            "value": "2 dot 5",
        }

        serializer = serializers.FieldValueSerializer(
            data=field_value_data, context={"field": field}
        )
        assert False is serializer.is_valid()
        msg = "A valid number is required."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_to_number_field_type(self):
        """
        Invalid number data on a number field raises validation error.
        """
        field = models.FieldName.objects.create(
            name="Dimension in square metres",
            field_type="number",
            risk_model=self.risk_model,
            order=1,
        )
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        field_value_data = {
            "form_submit": form_submit.id,
            "field": field.id,
            "value": "25.06",
        }

        serializer = serializers.FieldValueSerializer(
            data=field_value_data, context={"field": field}
        )
        assert False is serializer.is_valid()
        msg = "A valid integer is required."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_to_time_field_type(self):
        """
        Invalid time data on a time field raises validation error.
        """
        field = models.FieldName.objects.create(
            name="Time of Arrival",
            field_type="time",
            risk_model=self.risk_model,
            order=1,
        )
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        field_value_data = {
            "form_submit": form_submit.id,
            "field": field.id,
            "value": "12Noon",
        }

        serializer = serializers.FieldValueSerializer(
            data=field_value_data, context={"field": field}
        )
        assert False is serializer.is_valid()
        msg = "Time has wrong format."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_to_radio_field_type(self):
        """
        Invalid choice data on a radio field raises validation error.
        """
        field = models.FieldName.objects.create(
            name="Property",
            field_type="radio",
            choices=["Automobile", "Real Estate", "Equipment"],
            risk_model=self.risk_model,
            order=1,
        )
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        field_value_data = {
            "form_submit": form_submit.id,
            "field": field.id,
            "value": "Talent",
        }

        serializer = serializers.FieldValueSerializer(
            data=field_value_data, context={"field": field}
        )
        assert False is serializer.is_valid()
        msg = '"Talent" is not a valid choice.'
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_to_multiselect_field_type(self):
        """
        Invalid choice data on a multiselect field raises validation error.
        """
        field = models.FieldName.objects.create(
            name="Favorite Framework",
            field_type="multiselect",
            choices=["Django", "Flask", "Grok"],
            risk_model=self.risk_model,
            order=1,
        )
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        field_value_data = {
            "form_submit": form_submit.id,
            "field": field.id,
            "value": ["Express"],
        }

        serializer = serializers.FieldValueSerializer(
            data=field_value_data, context={"field": field}
        )
        assert False is serializer.is_valid()
        msg = '"Express" is not a valid choice.'
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_to_multiple_choice_field_type(self):
        """
        Invalid choices data on a multiselect field raises validation error.
        """
        field = models.FieldName.objects.create(
            name="Active Hours",
            field_type="multiselect",
            choices=[
                "00:00-3:00",
                "04:00-7:00",
                "08:00-11:00",
                "12:00-15:00",
                "16:00-19:00",
                "20:00-23:00",
            ],
            risk_model=self.risk_model,
            order=1,
        )
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        field_value_data = {
            "form_submit": form_submit.id,
            "field": field.id,
            "value": ["08:00-11:00", "12:00-15:00", "1600-19:00"],
        }

        serializer = serializers.FieldValueSerializer(
            data=field_value_data, context={"field": field}
        )
        assert False is serializer.is_valid()
        msg = '"1600-19:00" is not a valid choice.'
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_to_checkbox_field_type(self):
        """
        Invalid bool data on a checkbox field raises validation error.
        """
        field = models.FieldName.objects.create(
            name="Activated",
            field_type="checkbox",
            risk_model=self.risk_model,
            order=1,
        )
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        field_value_data = {
            "form_submit": form_submit.id,
            "field": field.id,
            "value": "Positive",
        }

        serializer = serializers.FieldValueSerializer(
            data=field_value_data, context={"field": field}
        )
        assert False is serializer.is_valid()
        msg = "Must be a valid boolean."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_to_url_field_type(self):
        """
        Invalid url data on a url field raises validation error.
        """
        field = models.FieldName.objects.create(
            name="Website",
            field_type="url",
            risk_model=self.risk_model,
            order=1,
        )
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        field_value_data = {
            "form_submit": form_submit.id,
            "field": field.id,
            "value": "www.techintel.dev",
        }

        serializer = serializers.FieldValueSerializer(
            data=field_value_data, context={"field": field}
        )
        assert False is serializer.is_valid()
        msg = "Enter a valid URL."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_to_regex_field_type(self):
        """
        asserts invalid url raises a validation error
        """
        field = models.FieldName.objects.create(
            name="Registration Code",
            field_type="regex",
            regex_pattern="^BRC",
            risk_model=self.risk_model,
            order=1,
        )
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        field_value_data = {
            "form_submit": form_submit.id,
            "field": field.id,
            "value": "BRD23456569875",
        }

        serializer = serializers.FieldValueSerializer(
            data=field_value_data, context={"field": field}
        )
        assert False is serializer.is_valid()
        msg = "This value does not match the required pattern."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_to_array_field_type(self):
        """
        Invalid array data on array field raises a validation error.
        """
        field = models.FieldName.objects.create(
            name="Hobbies",
            field_type="array",
            risk_model=self.risk_model,
            order=1,
        )
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        field_value_data = {
            "form_submit": form_submit.id,
            "field": field.id,
            "value": "dancing, coding",
        }

        serializer = serializers.FieldValueSerializer(
            data=field_value_data, context={"field": field}
        )
        assert False is serializer.is_valid()
        msg = 'Expected a list of items but got type "str".'
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_to_file_field_type(self):
        """
        Invalid file data to file field raises a validation error.
        """
        field = models.FieldName.objects.create(
            name="Passport Photo",
            field_type="file",
            risk_model=self.risk_model,
            order=1,
        )
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        field_value_data = {
            "form_submit": form_submit.id,
            "field": field.id,
            "value": "passport.jpg",
        }

        serializer = serializers.FieldValueSerializer(
            data=field_value_data, context={"field": field}
        )
        assert False is serializer.is_valid()
        msg = "The submitted data was not a file."
        with self.assertRaisesMessage(ValidationError, msg):
            serializer.is_valid(raise_exception=True)

    def test_field_type_file_valid_data_pass(self):
        """
        Serializer is valid with valid files.
        """
        field = models.FieldName.objects.create(
            name="Passport Photo",
            field_type="file",
            risk_model=self.risk_model,
            order=1,
        )
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        field_value_data = {
            "form_submit": form_submit.id,
            "field": field.id,
            "value": utils.generate_inmemory_text_file(),
        }
        serializer = serializers.FieldValueSerializer(
            data=field_value_data, context={"field": field}
        )
        assert True is serializer.is_valid()
        self.assertIsInstance(
            serializer.validated_data["value"], InMemoryUploadedFile
        )
