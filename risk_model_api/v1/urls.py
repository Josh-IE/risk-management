from django.urls import include, path
from rest_framework import routers

from . import views

# Create router and register viewsets.
router = routers.DefaultRouter()
router.register(r"risk_model", views.RiskModelViewSet, basename="risk_model")
router.register(r"risk_data", views.RiskDataViewSet, basename="risk_data")
router.register(
    r"risk_data_log", views.RiskDataLogViewSet, basename="risk_data_log"
)

# The API URLs are provided by the router.
app_name = "risk_model_api"
urlpatterns = [path("", include(router.urls))]
