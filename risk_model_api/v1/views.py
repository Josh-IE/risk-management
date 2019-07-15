from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .. import models
from ..utils import serializer_helpers
from . import serializers


class RiskModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    A ViewSet for listing, retrieving, creating and editing Risk Models
    """

    serializer_class = serializers.RiskModelSerializer
    queryset = models.RiskModel.objects.all().order_by("-id")

    @action(detail=False)
    def field_types(self, request):
        """
        route for fetching the list of field type choices
        """
        return Response(models.FieldName().field_choices())


class RiskDataViewSet(viewsets.ViewSet):
    """
    A ViewSet for creating and retrieving Risk Model data
    """

    def create(self, request):
        """
        creates a risk model's data
        """
        risk_data = serializer_helpers.RiskDataProcessor(request.data)
        serializer = serializers.RiskDataSerializer(
            data=risk_data.querydict_to_dict()
        )
        serializer.is_valid(raise_exception=True)
        risk_data.validated_data = serializer.validated_data
        return Response(
            risk_data.create_fields_data(), status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        """
        retrieves the submitted risk data from the FieldValue model
        """
        queryset = models.FieldValue.objects.filter(
            form_submit_id=pk
        ).order_by("id")
        return Response(
            serializers.FieldValueResponseSerializer(
                queryset, many=True, context={"request": request}
            ).data
        )


class RiskDataLogViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    A ViewSet for listing successful risk data submission events
    """

    serializer_class = serializers.RiskDataLogSerializer

    def get_queryset(self):
        """
        This view returns a list of all the successful risk data submission
        events by filtering against the risk_model portion of the URL.
        """
        queryset = models.FormSubmit.objects.filter(success=True).order_by(
            "-id"
        )
        risk_model = self.request.query_params.get("risk_model", None)
        if risk_model is not None:
            queryset = queryset.filter(risk_model=risk_model)
        return queryset
