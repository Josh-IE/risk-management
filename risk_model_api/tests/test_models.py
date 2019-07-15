from django.conf import settings
from django.core.validators import ValidationError
from django.test import TestCase

from .. import models
from ..utils import utils


class FieldNameTestCase(TestCase):
    """
    Unit tests for the RiskModel model.
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

    def test_min_length_validator(self):
        """
        min_length value cant be > FIELD_MAX_LENGTH.
        """
        field = models.FieldName.objects.create(
            name="Field 3",
            field_type="text",
            risk_model=self.risk_model,
            min_length=settings.FIELD_MAX_LENGTH + 1,
            order=3,
            deleted=True,
        )
        self.assertRaises(ValidationError, field.full_clean)

    def test_max_length_validator(self):
        """
        max_length value cant be > FIELD_MAX_LENGTH.
        """
        field = models.FieldName.objects.create(
            name="Field 4",
            field_type="text",
            risk_model=self.risk_model,
            max_length=settings.FIELD_MAX_LENGTH + 1,
            order=4,
            deleted=True,
        )
        self.assertRaises(ValidationError, field.full_clean)

    def test_non_deleted_objects_manager(self):
        """
        Deleted objects are excluded by the model manager.
        """
        self.assertEqual(len(models.FieldName.objects.all()), 1)

    def test_all_objects_manager(self):
        """
        Deleted objects are excluded by the model manager.
        """
        self.assertEqual(len(models.FieldName.all_objects.all()), 2)

    def test_slug_field_create(self):
        """
        slug field is autopopulated.
        """
        field = models.FieldName.objects.create(
            name="Field 5",
            field_type="text",
            risk_model=self.risk_model,
            max_length=settings.FIELD_MAX_LENGTH + 1,
            order=1,
        )
        self.assertIsNotNone(field.slug)

    def test_slug_field_max_length_limit(self):
        """
        The generated slug field is truncated to the max length attribute of
        the 'slug' field, if the concatenation of the slug and the incremental
        suffix exceeds the max length of the 'slug' field.
        """
        large_255_len_string = (
            "obbvyylmnkpbmyfutvaqubhuemhjnafmxlguvwondtvwradfvhoivkpklycsougxz"
            "apkyyzukfalmjmqotalnwcnkinuyogukbbjqvpzrytxcwnwzosthwyqntqasgwyrg"
            "zmyihozxkwxqgfiuqabhjxlabarokkbcjomnnqgscmpvorngxbihbegymlufsosqx"
            "yspqqbznzxdfkeggrrbujljedsayanwykayxxtctbdxdjbzkrimxblxaxcpm"
        )

        # generate first field instance with large_255_len_string as field name
        long_field_1 = models.FieldName.objects.create(
            name=large_255_len_string,
            field_type="text",
            risk_model=self.risk_model,
            order=1,
        )
        self.assertIsNotNone(long_field_1.slug)

        # generate 2nd field instance with large_255_len_string as field name
        long_field_2 = models.FieldName.objects.create(
            name=large_255_len_string,
            field_type="text",
            risk_model=self.risk_model,
            order=2,
        )
        self.assertIsNotNone(long_field_2.slug)
        self.assertNotEqual("long_field_1.slug", "long_field_2.slug")
        self.assertEqual(len(long_field_2.slug), 255)

    def test_field_choices(self):
        """
        The field types should be defined.
        """
        field_types = (
            ("array", "ARRAY"),
            ("checkbox", "CHECKBOX/BOOL"),
            ("date", "DATE"),
            ("email", "EMAIL"),
            ("file", "FILE"),
            ("float", "FLOAT"),
            ("multiselect", "MULTI SELECT/GROUP CHECKBOX"),
            ("number", "NUMBER"),
            ("password", "PASSWORD"),
            ("radio", "RADIO"),
            ("regex", "REGEX"),
            ("select", "SELECT"),
            ("switch", "SWITCH"),
            ("text", "TEXT"),
            ("textarea", "TEXT AREA"),
            ("time", "TIME"),
            ("url", "URL"),
        )
        self.assertEqual(field_types, models.FIELD_TYPES)
        self.assertEqual(
            utils.tuple_to_dict(field_types),
            models.FieldName().field_choices(),
        )
