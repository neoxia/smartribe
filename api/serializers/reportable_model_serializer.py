from rest_framework import serializers


class ReportableModelSerializer(serializers.ModelSerializer):

    reference = serializers.CharField(source='get_report_information', read_only=True)
