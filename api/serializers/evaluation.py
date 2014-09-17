from rest_framework import serializers
from api.serializers.reportable_model_serializer import ReportableModelSerializer

from core.models import Evaluation


class EvaluationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evaluation
        exclude = ('creation_date', 'last_update')


class EvaluationSerializer(ReportableModelSerializer):

    class Meta:
        model = Evaluation
        read_only_fields = ('meeting', 'creation_date', 'last_update')
