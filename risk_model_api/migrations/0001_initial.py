import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="RiskModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("button", models.CharField(max_length=255)),
                ("success_msg", models.TextField(null=True)),
                ("activated", models.BooleanField(default=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "client",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="risk_model_api.Client",
                    ),
                ),
                ("description", models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="FormSubmit",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "risk_model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="risk_model_api.RiskModel",
                    ),
                ),
                ("success", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="FieldName",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.CharField(max_length=255)),
                (
                    "field_type",
                    models.CharField(
                        choices=[
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
                        ],
                        max_length=255,
                    ),
                ),
                ("required", models.BooleanField(default=True)),
                ("help_text", models.TextField(null=True)),
                (
                    "order",
                    models.PositiveIntegerField(
                        verbose_name=django.core.validators.MinValueValidator(
                            1
                        )
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "risk_model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="fields",
                        to="risk_model_api.RiskModel",
                    ),
                ),
                (
                    "choices",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=255),
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "default",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("deleted", models.BooleanField(default=False)),
                (
                    "max_length",
                    models.PositiveIntegerField(
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(1000),
                        ],
                    ),
                ),
                (
                    "min_length",
                    models.PositiveIntegerField(
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(1000),
                        ],
                    ),
                ),
                ("unique", models.BooleanField(default=False)),
                (
                    "regex_pattern",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FieldValue",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.CharField(max_length=1000, null=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="risk_model_api.FieldName",
                    ),
                ),
                (
                    "form_submit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="risk_model_api.FormSubmit",
                    ),
                ),
            ],
        ),
    ]
