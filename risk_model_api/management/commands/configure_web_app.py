import sys
from django.core.management.base import BaseCommand
from django.core.management import call_command

from risk_model_api import models

RISK_MODEL_APP = "risk_model_api"
RISK_MODEL_MODELS_TO_WIPE = [
    models.FieldValue,
    models.FormSubmit,
    models.FieldName,
    models.RiskModel,
    models.Client,
]


class Command(BaseCommand):
    help = "Setup for the BriteCore Web App."

    def handle(self, *args, **kwargs):
        self._load_fixtures()
        self.stdout.write("Setup complete")

    def _error(self, e, doexit=False):
        self.stdout.write(self.style.ERROR(e))
        if doexit:
            sys.exit(1)

    def _load_fixtures(self):
        fixtures = ["app_data"]
        try:
            self._truncate_tables()
            self.stdout.write("Loading fixtures")
            call_command("loaddata", *fixtures, app=RISK_MODEL_APP)
            self.stdout.write(
                self.style.SUCCESS("RISK_MODEL_APP fixtures loaded")
            )
        except Exception as e:
            self._error("Error loading fixtures:\n{}".format(str(e)), True)

    def _truncate_tables(self):
        self.stdout.write("Truncating tables")
        try:
            for m in RISK_MODEL_MODELS_TO_WIPE:
                if m.__name__ == "FieldName":
                    m.all_objects.all().delete()
                else:
                    m.objects.all().delete()
        except Exception as e:
            self._error("Error truncating tables:\n{}".format(str(e)), True)
