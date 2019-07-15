from django.conf import settings
from django.http import QueryDict
from django.test import TestCase, override_settings

from botocore.exceptions import ParamValidationError

from .. import models as models
from ..utils import utils


class UtilsTestCase(TestCase):
    """
    Unit tests for the Utils module.
    """

    def test_tuple_to_dict(self):
        """
        The tuple_to_dict function should return the expected output.
        """
        sample_tuple = (
            ("django", "DJANGO"),
            ("flask", "FLASK"),
            ("grok", "GROK"),
        )
        expected_list = [
            {"text": "DJANGO", "value": "django"},
            {"text": "FLASK", "value": "flask"},
            {"text": "GROK", "value": "grok"},
        ]
        response = utils.tuple_to_dict(sample_tuple)
        self.assertEqual(response, expected_list)

    def test_nested_field_parse(self):
        """
        The nested_field_parse() should return a flat dict when a nested
        Querydict is passed.
        """

        sample_querydict_data = {
            "risk_model": 2,
            "risk_model_name": "Insurance",
            "data[name]": "Joshua",
            "data[email]": "Joshua@techintel.dev",
            "data[repositories]": 18,
        }

        sample_querydict = QueryDict(mutable=True)
        sample_querydict.update(sample_querydict_data)

        expected_dict = {
            "risk_model": 2,
            "risk_model_name": "Insurance",
            "data": {
                "name": "Joshua",
                "email": "Joshua@techintel.dev",
                "repositories": 18,
            },
        }
        response = utils.nested_field_parse(sample_querydict)
        self.assertEqual(response, expected_dict)

    def test_generate_unique_slug(self):
        """
        The generate_unique_slug() method should return a unique slug.
        """
        # create client
        client = models.Client.objects.create(name="Client 1")
        # create risk model
        risk_model = models.RiskModel.objects.create(
            client=client, name="Risk Model 1", button="Save"
        )
        # create field
        obj = models.FieldName.objects.create(
            name="Field 1",
            field_type="text",
            risk_model=risk_model,
            max_length=settings.FIELD_MAX_LENGTH + 1,
            order=1,
        )

        # value to be slugified
        value = "Country of Residence"
        slug_1 = utils.generate_unique_slug(models.FieldName, value)

        # overwrite slug field, with value
        obj.slug = slug_1
        obj.save()

        # create 2nd slug with the same value
        slug_2 = utils.generate_unique_slug(models.FieldName, value)

        # assert 2nd slug is different from 1st slug
        self.assertNotEqual(slug_1, slug_2)

    def test_generate_inmemory_text_file(self):
        """
        The inmemory_text_file() util should return an inmemory file object.
        """
        file_name = "new_file.txt"
        file = utils.generate_inmemory_text_file(file_name)
        self.assertEqual(file._get_name(), file_name)

    @override_settings(
        DEFAULT_FILE_STORAGE="some_storage", YOUR_S3_BUCKET="fakebucket"
    )
    def test_store_file(self):
        """
        s3 storage is used when the default django storage is not used.
        """
        file_name = "new_file.txt"
        file = utils.generate_inmemory_text_file(file_name)
        msg = (
            'Invalid bucket name "": Bucket name must match the regex '
            r'"^[a-zA-Z0-9.\-_]{1,255}$"'
        )
        with self.assertRaisesMessage(ParamValidationError, msg):
            utils.store_file(file)
