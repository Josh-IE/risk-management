from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from .. import models
from ..utils import utils
from ..v1 import views


class RiskModelViewSetTest(TestCase):
    """
    Unit tests for the Risk Model view.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        # create client
        client = models.Client.objects.create(name="Client 1")
        # create risk model
        self.risk_model = models.RiskModel.objects.create(
            client=client, name="Risk Model 1", button="Save"
        )

        # create fields
        self.normal_field_1 = models.FieldName.objects.create(
            name="Field 1",
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

        # create a soft deleted field
        self.deleted_field = models.FieldName.objects.create(
            name="Field 3",
            field_type="text",
            risk_model=self.risk_model,
            order=3,
            deleted=True,
        )

    def test_list_risk_models(self):
        """
        A 200 status is returned by the risk model list view.
        The list of risk models are returned by the risk_model-list.
        """
        url = reverse("risk_model:risk_model-list")
        request = self.factory.get(url)
        response = views.RiskModelViewSet.as_view({"get": "list"})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_risk_model_with_fields(self):
        """
        A 201 is returned by the risk model create view.
        POST requests to risk_model-list creates a riskmodel with fields.
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
                "order": 1,
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
                "order": 2,
            },
        ]

        data = {
            "name": "Auto Insurance",
            "button": "Create",
            "activated": True,
            "fields": field_data,
        }

        # update/put request
        url = reverse("risk_model:risk_model-list")
        request = self.factory.post(url, data, format="json")
        response = views.RiskModelViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_field_keys = set(
            [
                "id",
                "name",
                "slug",
                "field_type",
                "default",
                "regex_pattern",
                "min_length",
                "max_length",
                "choices",
                "required",
                "help_text",
                "order",
                "unique",
            ]
        )
        self.assertEqual(
            expected_field_keys, set(response.data["fields"][0].keys())
        )
        self.assertEqual(len(response.data["fields"]), 2)

    def test_create_risk_model_without_fields(self):
        """
        A 400 is returned when creating a risk model without fields.
        """
        data = {
            "name": "Auto Insurance",
            "button": "Create",
            "activated": True,
            "fields": [],
        }

        # post request
        url = reverse("risk_model:risk_model-list")
        request = self.factory.post(url, data, format="json")
        response = views.RiskModelViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("fields", response.data)
        self.assertIn(
            "Risk Model has no fields. At least one field is required.",
            response.data["fields"][0],
        )

    def test_new_field_slug_is_ignored(self):
        """
        New field 'slug' is ignored, if provided in request.
        """
        data = {
            "name": "Auto Insurance",
            "button": "Create",
            "activated": True,
            "fields": [
                {
                    "name": "Location",
                    "field_type": "text",
                    "slug": "address",
                    "default": "World Wide",
                    "min_length": 5,
                    "max_length": 10,
                    "choices": None,
                    "required": True,
                    "help_text": "Where are you located?",
                    "order": 1,
                }
            ],
        }

        # update/put request
        url = reverse("risk_model:risk_model-list")
        request = self.factory.post(url, data, format="json")
        response = views.RiskModelViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("slug", response.data["fields"][0])
        self.assertNotEqual(
            response.data["fields"][0]["slug"], data["fields"][0]["slug"]
        )

    def test_new_field_id_is_ignored(self):
        """
        New field 'id' is ignored if provided in request.
        """
        data = {
            "name": "Auto Insurance",
            "button": "Create",
            "activated": True,
            "fields": [
                {
                    "id": 200,
                    "name": "Location",
                    "field_type": "text",
                    "default": "World Wide",
                    "min_length": 5,
                    "max_length": 10,
                    "choices": None,
                    "required": True,
                    "help_text": "Where are you located?",
                    "order": 1,
                }
            ],
        }

        # update/put request
        url = reverse("risk_model:risk_model-list")
        request = self.factory.post(url, data, format="json")
        response = views.RiskModelViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data["fields"][0])
        self.assertNotEqual(
            response.data["fields"][0]["id"], data["fields"][0]["id"]
        )

    def test_risk_model_retrieve(self):
        """
        A 200 status is returned by the risk model retrieve view.
        The risk model object is returned by the retrieve view.
        """
        url = reverse(
            "risk_model:risk_model-detail", args=[self.risk_model.id]
        )
        request = self.factory.get(url)
        response = views.RiskModelViewSet.as_view({"get": "retrieve"})(
            request, pk=self.risk_model.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_risk_model_update(self):
        """
        A 200 status is returned by the risk model update view.
        The riskmodel is updated by the update view.
        """
        updated_data = {
            "name": "Location",
            "button": "Create",
            "description": "Registration Form",
            "success_msg": "Congrats. Check your mail",
            "activated": False,
            "fields": [
                {
                    "name": "Location",
                    "field_type": "text",
                    "default": "World Wide",
                    "regex_pattern": None,
                    "min_length": 5,
                    "max_length": 10,
                    "choices": None,
                    "required": True,
                    "help_text": "Where are you located?",
                    "order": 1,
                    "unique": False,
                }
            ],
        }

        # update/put request
        url = reverse(
            "risk_model:risk_model-detail", args=[self.risk_model.id]
        )
        request = self.factory.put(url, updated_data, format="json")
        updated_response = views.RiskModelViewSet.as_view({"put": "update"})(
            request, pk=self.risk_model.id
        )
        self.assertEqual(updated_response.status_code, status.HTTP_200_OK)
        updated_response = dict(updated_response.data)
        updated_response.pop("id")
        updated_response["fields"][0].pop("id")
        updated_response["fields"][0].pop("slug")
        self.assertDictEqual(updated_response, updated_data)

    def test_list_risk_model_fields(self):
        """
        The risk model fields are returned by the retrieve view.
        Fields marked as deleted are excluded from the response.
        """
        url = reverse(
            "risk_model:risk_model-detail", args=[self.risk_model.id]
        )
        request = self.factory.get(url)
        response = views.RiskModelViewSet.as_view({"get": "retrieve"})(
            request, pk=self.risk_model.id
        )
        self.assertEqual(len(response.data["fields"]), 2)

    def test_update_risk_model_field_attribute(self):
        """
        The risk model field attributes are updated by the update view.
        """
        updated_field_name = "Number of Children"
        field_type = "number"
        no_of_children = "3"

        # initial retrieve request
        url = reverse(
            "risk_model:risk_model-detail", args=[self.risk_model.id]
        )
        request = self.factory.get(url)
        response = views.RiskModelViewSet.as_view({"get": "retrieve"})(
            request, pk=self.risk_model.id
        )

        # assert field len was initially 2
        self.assertEqual(len(response.data["fields"]), 2)

        updated_data = dict(response.data)
        updated_data["fields"][0]["name"] = "Number of Children"
        updated_data["fields"][0]["field_type"] = field_type
        updated_data["fields"][0]["default"] = no_of_children

        # update/put request
        url = reverse(
            "risk_model:risk_model-detail", args=[self.risk_model.id]
        )
        request = self.factory.put(url, updated_data, format="json")
        updated_response = views.RiskModelViewSet.as_view({"put": "update"})(
            request, pk=self.risk_model.id
        )
        self.assertEqual(updated_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(updated_response.data["fields"]), 2)
        self.assertEqual(
            updated_response.data["fields"][0]["name"], updated_field_name
        )
        self.assertEqual(
            updated_response.data["fields"][0]["field_type"], field_type
        )
        self.assertEqual(
            updated_response.data["fields"][0]["default"], str(no_of_children)
        )

    def test_update_risk_model_fields(self):
        """
        New nested fields are added to the risk model through the update view.
        """
        field_data = {
            "name": "Location",
            "field_type": "text",
            "default": "World Wide",
            "min_length": 5,
            "max_length": 10,
            "choices": None,
            "required": True,
            "help_text": "Where are you located?",
            "order": 3,
        }

        # initial retrieve request
        url = reverse(
            "risk_model:risk_model-detail", args=[self.risk_model.id]
        )
        request = self.factory.get(url)
        response = views.RiskModelViewSet.as_view({"get": "retrieve"})(
            request, pk=self.risk_model.id
        )

        # assert field len was initially 2
        self.assertEqual(len(response.data["fields"]), 2)

        updated_data = dict(response.data)
        updated_data["fields"].append(field_data)

        # update/put request
        url = reverse(
            "risk_model:risk_model-detail", args=[self.risk_model.id]
        )
        request = self.factory.put(url, updated_data, format="json")
        updated_response = views.RiskModelViewSet.as_view({"put": "update"})(
            request, pk=self.risk_model.id
        )
        self.assertEqual(updated_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(updated_response.data["fields"]), 3)

    def test_delete_risk_model_field(self):
        """
        Excluded nested fields are deleted from the risk model through the
        update view.
        """
        # initial retrieve request
        url = reverse(
            "risk_model:risk_model-detail", args=[self.risk_model.id]
        )
        request = self.factory.get(url)
        response = views.RiskModelViewSet.as_view({"get": "retrieve"})(
            request, pk=self.risk_model.id
        )

        # assert field len was initially 2
        self.assertEqual(len(response.data["fields"]), 2)

        updated_data = dict(response.data)
        updated_data["fields"].pop()

        # update/put request
        url = reverse(
            "risk_model:risk_model-detail", args=[self.risk_model.id]
        )
        request = self.factory.put(url, updated_data, format="json")
        updated_response = views.RiskModelViewSet.as_view({"put": "update"})(
            request, pk=self.risk_model.id
        )

        # assert field len is now 1
        self.assertEqual(len(updated_response.data["fields"]), 1)

    def test_delete_protected_risk_model_field(self):
        """
        Excluded nested fields, referenced by prior submitted data, are
        succesfully deleted by the update view.
        """
        # initial retrieve request
        url = reverse(
            "risk_model:risk_model-detail", args=[self.risk_model.id]
        )
        request = self.factory.get(url)
        response = views.RiskModelViewSet.as_view({"get": "retrieve"})(
            request, pk=self.risk_model.id
        )

        # assert field len was initially 2
        self.assertEqual(len(response.data["fields"]), 2)

        # create a Data Submission on the RiskModel Fields
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        risk_data = [
            models.FieldValue(
                form_submit=form_submit,
                field=self.normal_field_1,
                value="josh",
            ),
            models.FieldValue(
                form_submit=form_submit,
                field=self.normal_field_2,
                value="josh@brite.core",
            ),
        ]
        models.FieldValue.objects.bulk_create(risk_data)

        updated_data = dict(response.data)
        updated_data["fields"].pop()

        # update/put request
        url = reverse(
            "risk_model:risk_model-detail", args=[self.risk_model.id]
        )
        request = self.factory.put(url, updated_data, format="json")
        updated_response = views.RiskModelViewSet.as_view({"put": "update"})(
            request, pk=self.risk_model.id
        )

        # assert field len is now 1
        self.assertEqual(len(updated_response.data["fields"]), 1)
        self.assertEqual(
            updated_response.data["fields"][0]["name"],
            self.normal_field_1.name,
        )

    def test_create_risk_model_field_with_invalid_min_length(self):
        """
        A 400 status is returned if the min_length of the field is above bound.
        """
        field_data = [
            {
                "name": "Location",
                "field_type": "text",
                "default": "World Wide",
                "min_length": settings.FIELD_MAX_LENGTH + 1,
                "choices": None,
                "required": True,
                "help_text": "Where are you located?",
                "order": 1,
                "deleted": False,
            }
        ]

        data = {
            "name": "Auto Insurance",
            "button": "Create",
            "activated": True,
            "fields": field_data,
        }

        # update/put request
        url = reverse("risk_model:risk_model-list")
        request = self.factory.post(url, data, format="json")
        response = views.RiskModelViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("min_length", response.data["fields"][0])

    def test_create_risk_model_field_with_invalid_max_length(self):
        """
        A 400 status is returned if the max_length of the field is above bound.
        """
        field_data = [
            {
                "name": "Location",
                "field_type": "text",
                "default": "World Wide",
                "max_length": settings.FIELD_MAX_LENGTH + 1,
                "choices": None,
                "required": True,
                "help_text": "Where are you located?",
                "order": 1,
                "deleted": False,
            }
        ]

        data = {
            "name": "Auto Insurance",
            "button": "Create",
            "activated": True,
            "fields": field_data,
        }

        # update/put request
        url = reverse("risk_model:risk_model-list")
        request = self.factory.post(url, data, format="json")
        response = views.RiskModelViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("max_length", response.data["fields"][0])

    def test_get_field_type_choices_list(self):
        """
        The field_type choices are returned by the risk_model-field-types
        retrieve view.
        """
        url = reverse("risk_model:risk_model-field-types")
        request = self.factory.get(url)
        response = views.RiskModelViewSet.as_view({"get": "field_types"})(
            request
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, models.FieldName().field_choices())


class RiskDataViewSetTest(TestCase):
    """
    Unit tests for the Risk Data view.
    """

    def setUp(self):
        self.factory = APIRequestFactory()

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
        # log form submission
        self.form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )
        # create risk data
        self.data = [
            models.FieldValue(
                form_submit=self.form_submit,
                field=self.normal_field_1,
                value="Brite",
            ),
            models.FieldValue(
                form_submit=self.form_submit,
                field=self.normal_field_2,
                value="john@britecore.com",
            ),
            models.FieldValue(
                form_submit=self.form_submit,
                field=self.normal_field_3,
                value=25,
            ),
        ]
        self.risk_data_1 = models.FieldValue.objects.bulk_create(self.data)

    def test_risk_data_create(self):
        """
        A 201 is returned by the risk data create view.
        POST requests to risk_data-list creates risk data.
        """
        risk_data = {
            "risk_model": self.risk_model.id,
            "risk_model_name": self.risk_model.name,
            "data": {
                self.normal_field_1.slug: "Joshua",
                self.normal_field_2.slug: "josh@techintel.dev",
                self.normal_field_3.slug: 18,
            },
        }
        url = reverse("risk_model:risk_data-list")
        request = self.factory.post(url, risk_data, format="json")
        response = views.RiskDataViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["form_submit"])

    def test_create_risk_data_with_invalid_field_type(self):
        """
        A 400 status is returned by the risk data create view when risk data
        is created against an invalid field type.
        """
        # create invalid field type
        invalid_field = models.FieldName.objects.create(
            name="Mobile Number",
            field_type="phone",
            risk_model=self.risk_model,
            order=4,
        )
        risk_data = {
            "risk_model": self.risk_model.id,
            "risk_model_name": self.risk_model.name,
            "data": {
                self.normal_field_1.slug: "Joshua",
                self.normal_field_2.slug: "josh@techintel.dev",
                self.normal_field_3.slug: 18,
                invalid_field.slug: "+234800000000",
            },
        }
        url = reverse("risk_model:risk_data-list")
        request = self.factory.post(url, risk_data, format="json")
        response = views.RiskDataViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("fields", response.data)
        self.assertIn(
            "phone is not a valid field type", response.data["fields"][0]
        )

    def test_create_risk_data_with_invalid_field_value(self):
        """
        A 400 status is returned by the risk data create view when risk data
        is created with an invalid value.
        """
        # create invalid field type
        date_field = models.FieldName.objects.create(
            name="date", field_type="date", risk_model=self.risk_model, order=4
        )
        risk_data = {
            "risk_model": self.risk_model.id,
            "risk_model_name": self.risk_model.name,
            "data": {
                self.normal_field_1.slug: "Joshua",
                self.normal_field_2.slug: "josh@techintel.dev",
                self.normal_field_3.slug: 18,
                date_field.slug: "April272006",
            },
        }
        url = reverse("risk_model:risk_data-list")
        request = self.factory.post(url, risk_data, format="json")
        response = views.RiskDataViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date", response.data)
        self.assertIn("Date has wrong format", response.data["date"][0])

    def test_create_risk_data_with_file_field_type(self):
        """
        A 201 status is returned by the risk data create view, when a file is
        sent with data.
        POST request with file to risk_data-list creates the risk data.
        """
        file_field = models.FieldName.objects.create(
            name="Purchase Document",
            field_type="file",
            risk_model=self.risk_model,
            order=4,
        )

        risk_data = {
            "risk_model": self.risk_model.id,
            "risk_model_name": self.risk_model.name,
            f"data[{self.normal_field_1.slug}]": "Joshua",
            f"data[{self.normal_field_2.slug}]": "josh@techintel.dev",
            f"data[{self.normal_field_3.slug}]": 18,
            f"data[{file_field.slug}]": utils.generate_inmemory_text_file(),
        }
        url = reverse("risk_model:risk_data-list")
        request = self.factory.post(url, risk_data, format="multipart")
        response = views.RiskDataViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["form_submit"])

    def test_create_empty_risk_data_with_checkbox_field_type(self):
        """
        False is stored if the posted checkbox data is an empty string.
        """
        checkbox_field = models.FieldName.objects.create(
            name="First time attending Pycon?",
            field_type="checkbox",
            risk_model=self.risk_model,
            order=4,
        )

        risk_data = {
            "risk_model": self.risk_model.id,
            "risk_model_name": self.risk_model.name,
            f"data[{self.normal_field_1.slug}]": "Joshua",
            f"data[{self.normal_field_2.slug}]": "josh@techintel.dev",
            f"data[{self.normal_field_3.slug}]": 18,
            f"data[{checkbox_field.slug}]": "",
        }
        url = reverse("risk_model:risk_data-list")
        request = self.factory.post(url, risk_data)
        response = views.RiskDataViewSet.as_view({"post": "create"})(request)
        stored_value = models.FieldValue.objects.get(
            form_submit_id=response.data["form_submit"], field=checkbox_field
        ).value
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["form_submit"])
        self.assertEqual("False", stored_value)

    def test_create_risk_data_with_file_and_array_field_type(self):
        """
        A 201 is returned by the risk data create view.
        POST request with file and array fields to risk_data-list is
        successfully parsed and risk data is created.
        """
        file_field = models.FieldName.objects.create(
            name="Purchase Document",
            field_type="file",
            risk_model=self.risk_model,
            order=4,
        )
        array_field = models.FieldName.objects.create(
            name="Hobbies",
            field_type="array",
            risk_model=self.risk_model,
            order=4,
        )

        risk_data = {
            "risk_model": self.risk_model.id,
            "risk_model_name": self.risk_model.name,
            f"data[{self.normal_field_1.slug}]": "Joshua",
            f"data[{self.normal_field_2.slug}]": "josh@techintel.dev",
            f"data[{self.normal_field_3.slug}]": 18,
            f"data[{array_field.slug}][]": ["coding", "laughing"],
            f"data[{file_field.slug}]": utils.generate_inmemory_text_file(),
        }
        url = reverse("risk_model:risk_data-list")
        request = self.factory.post(url, risk_data, format="multipart")
        response = views.RiskDataViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["form_submit"])

    def test_risk_data_retrieve(self):
        """
        A 200 status is returned by the risk data retrieve view.
        The risk data is returned by the retrieve view.
        """
        url = reverse(
            "risk_model:risk_data-detail", args=[self.form_submit.id]
        )
        request = self.factory.get(url)
        response = views.RiskDataViewSet.as_view({"get": "retrieve"})(
            request, pk=self.form_submit.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]["value"], "Brite")
        self.assertEqual(response.data[1]["value"], "john@britecore.com")
        self.assertEqual(response.data[2]["value"], "25")

    def test_retrieve_risk_data_file_url(self):
        """
        The url of 'file' field types are available in the retrieved risk data.
        """
        # create file field
        file_field = models.FieldName.objects.create(
            name="Purchase Document",
            field_type="file",
            risk_model=self.risk_model,
            order=4,
        )

        # make a create risk data request
        risk_data = {
            "risk_model": self.risk_model.id,
            "risk_model_name": self.risk_model.name,
            f"data[{self.normal_field_1.slug}]": "Brite",
            f"data[{self.normal_field_2.slug}]": "john@britecore.com",
            f"data[{self.normal_field_3.slug}]": 25,
            f"data[{file_field.slug}]": utils.generate_inmemory_text_file(),
        }
        url = reverse("risk_model:risk_data-list")
        request = self.factory.post(url, risk_data, format="multipart")
        response = views.RiskDataViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["form_submit"])

        # host settings
        host = "192.168.0.1"

        # make a retrieve risk data request and verify file url
        url = reverse(
            "risk_model:risk_data-detail", args=[response.data["form_submit"]]
        )
        request = self.factory.get(url, args=[response.data["form_submit"]])
        request.META["HTTP_HOST"] = host
        retrieve_response = views.RiskDataViewSet.as_view({"get": "retrieve"})(
            request, pk=response.data["form_submit"]
        )

        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(retrieve_response.data), 4)
        self.assertEqual(retrieve_response.data[0]["value"], "Brite")
        self.assertEqual(
            retrieve_response.data[1]["value"], "john@britecore.com"
        )
        self.assertEqual(retrieve_response.data[2]["value"], "25")
        self.assertRegex(
            retrieve_response.data[3]["value"],
            r"^http://192.168.0.1/media/foo\w*.txt$",
        )

    @override_settings(
        DEFAULT_FILE_STORAGE="some_storage",
        YOUR_S3_BUCKET="fakebucket",
        STATIC_URL="https://fakebucket.s3.amazonaws.com/",
    )
    def test_retrieve_risk_data_file_url_with_non_django_storage(self):
        """
        The AWS bucket url is used as the file media url in risk data retrieve
        requests, when the default django storage is not used.
        """
        # create file field
        file_field = models.FieldName.objects.create(
            name="Purchase Document",
            field_type="file",
            risk_model=self.risk_model,
            order=4,
        )

        # log form submission
        form_submit = models.FormSubmit.objects.create(
            risk_model=self.risk_model, success=True
        )

        risk_data = [
            models.FieldValue(
                form_submit=form_submit,
                field=self.normal_field_1,
                value="Brite",
            ),
            models.FieldValue(
                form_submit=form_submit,
                field=self.normal_field_2,
                value="john@britecore.com",
            ),
            models.FieldValue(
                form_submit=form_submit, field=self.normal_field_3, value=25
            ),
            models.FieldValue(
                form_submit=form_submit, field=file_field, value="abcde.txt"
            ),
        ]
        models.FieldValue.objects.bulk_create(risk_data)

        # make a retrieve risk data request and verify file url
        url = reverse("risk_model:risk_data-detail", args=[form_submit.id])
        request = self.factory.get(url, args=[form_submit.id])
        retrieve_response = views.RiskDataViewSet.as_view({"get": "retrieve"})(
            request, pk=form_submit.id
        )

        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(retrieve_response.data), 4)
        self.assertEqual(retrieve_response.data[0]["value"], "Brite")
        self.assertEqual(
            retrieve_response.data[1]["value"], "john@britecore.com"
        )
        self.assertEqual(retrieve_response.data[2]["value"], "25")
        self.assertRegex(
            retrieve_response.data[3]["value"], f"^{settings.STATIC_URL}"
        )


class RiskDataLogViewSetTest(TestCase):
    """
    Unit tests for Risk Data Log view.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        # create client
        client = models.Client.objects.create(name="Client 1")
        # create risk model
        self.risk_model_1 = models.RiskModel.objects.create(
            client=client, name="Risk Model 1", button="Save"
        )
        self.risk_model_2 = models.RiskModel.objects.create(
            client=client, name="Risk Model 2", button="Create"
        )
        # create fields for Risk Model 1
        self.normal_field_1 = models.FieldName.objects.create(
            name="First Name",
            field_type="text",
            risk_model=self.risk_model_1,
            order=1,
        )
        self.normal_field_2 = models.FieldName.objects.create(
            name="Email",
            field_type="email",
            risk_model=self.risk_model_1,
            order=2,
        )
        self.normal_field_3 = models.FieldName.objects.create(
            name="Age",
            field_type="number",
            risk_model=self.risk_model_1,
            order=3,
        )
        # Create fields for Risk Model 2
        self.normal_field_4 = models.FieldName.objects.create(
            name="First Name",
            field_type="text",
            risk_model=self.risk_model_2,
            order=1,
        )
        self.normal_field_5 = models.FieldName.objects.create(
            name="Email",
            field_type="email",
            risk_model=self.risk_model_2,
            order=2,
        )
        # log form submission for risk_model_1
        self.form_submit_1 = models.FormSubmit.objects.create(
            risk_model=self.risk_model_1, success=True
        )
        self.form_submit_2 = models.FormSubmit.objects.create(
            risk_model=self.risk_model_1, success=True
        )
        self.form_submit_3 = models.FormSubmit.objects.create(
            risk_model=self.risk_model_1, success=False
        )
        self.form_submit_4 = models.FormSubmit.objects.create(
            risk_model=self.risk_model_2, success=False
        )
        self.form_submit_5 = models.FormSubmit.objects.create(
            risk_model=self.risk_model_2, success=True
        )
        self.form_submit_6 = models.FormSubmit.objects.create(
            risk_model=self.risk_model_2, success=True
        )
        self.form_submit_7 = models.FormSubmit.objects.create(
            risk_model=self.risk_model_2, success=True
        )

    def test_risk_data_log_list(self):
        """
        All the logs of successful risk data submissions, are returned by the
        risk_data_log list view.
        """
        url = reverse("risk_model:risk_data_log-list")
        request = self.factory.get(url)
        response = views.RiskDataLogViewSet.as_view({"get": "list"})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_risk_model_risk_data_log_list(self):
        """
        All the logs of successful risk data submissions on a risk model,
        are returned by the risk_data_log list view.
        """
        url = reverse("risk_model:risk_data_log-list")
        data = {"risk_model": self.risk_model_2.id}
        request = self.factory.get(url, data)
        response = views.RiskDataLogViewSet.as_view({"get": "list"})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
