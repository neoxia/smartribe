from rest_framework import serializers
from api.serializers.reportable_model_serializer import ReportableModelSerializer

from core.models import Evaluation


class EvaluationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evaluation
        exclude = ('creation_date', 'last_update')


class EvaluationSerializer(ReportableModelSerializer):

    had_meeting = serializers.BooleanField(source='had_meeting', read_only=True)

    class Meta:
        model = Evaluation
        read_only_fields = ('offer', 'creation_date', 'last_update')
