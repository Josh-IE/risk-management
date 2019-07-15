from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .utils import utils

FIELD_TYPES = (
    ("array", "ARRAY"),
    ("checkbox", "CHECKBOX/BOOL"),
    ("date", "DATE"),
    ("email", "EMAIL"),
    ("file", "FILE"),
    ("float", "FLOAT"),
    # ('hidden', 'HIDDEN'), #deprioritized
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


class Client(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = "risk_model_api"


class RiskModel(models.Model):
    """
    Risk type model.
    """
    client = models.ForeignKey("Client", null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    success_msg = models.TextField(null=True)
    button = models.CharField(max_length=255)
    activated = models.BooleanField(default=True)
    # deleted = models.BooleanField(
    #     default=False
    # )  # not implemented: deprioritized
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "risk_model_api"


class NonDeletedFieldManager(models.Manager):
    """
    Filters out Fields marked as deleted.
    """

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class DefaultFieldManager(models.Manager):
    """
    Returns all Fields.
    """

    def get_queryset(self):
        return super().get_queryset()


class FieldName(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    field_type = models.CharField(max_length=255, choices=FIELD_TYPES)
    default = models.CharField(max_length=255, blank=True, null=True)
    regex_pattern = models.CharField(max_length=255, blank=True, null=True)
    min_length = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(settings.FIELD_MAX_LENGTH),
        ],
        null=True,
    )
    max_length = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(settings.FIELD_MAX_LENGTH),
        ],
        null=True,
    )
    # for numerical fields
    # min_value = models.IntegerField(
    #     null=True)
    # max_value = models.IntegerField(
    #     null=True) # not implemented: deprioritized
    choices = ArrayField(models.CharField(max_length=255), null=True)
    risk_model = models.ForeignKey(
        "RiskModel", related_name="fields", on_delete=models.PROTECT
    )
    required = models.BooleanField(default=True)
    help_text = models.TextField(null=True)
    order = models.PositiveIntegerField(MinValueValidator(1))
    unique = models.BooleanField(default=False)
    # disabled = models.BooleanField(
    #     default=False) # not implemented: depriorititized
    deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = NonDeletedFieldManager()
    all_objects = DefaultFieldManager()

    class Meta:
        app_label = "risk_model_api"

    @classmethod
    def field_choices(cls):
        """
        returns the Field types as a list of 'text' & 'value' keyed dicts.
        """
        return utils.tuple_to_dict(FIELD_TYPES)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = utils.generate_unique_slug(FieldName, self.name)
        super(FieldName, self).save(*args, **kwargs)


class FormSubmit(models.Model):
    """
    Logs risk form submission events
    """

    risk_model = models.ForeignKey("RiskModel", on_delete=models.PROTECT)
    success = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "risk_model_api"


class FieldValue(models.Model):
    """
    Stores the user submitted values
    """

    form_submit = models.ForeignKey("FormSubmit", on_delete=models.PROTECT)
    field = models.ForeignKey("FieldName", on_delete=models.PROTECT)
    value = models.CharField(max_length=settings.FIELD_MAX_LENGTH, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "risk_model_api"
