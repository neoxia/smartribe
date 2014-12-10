from rest_framework import serializers
from core.models import SkillCategory, Skill


class SkillCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SkillCategory


class SkillCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill


class SkillSerializer(serializers.ModelSerializer):

    mark_count = serializers.IntegerField(source='get_mark_count', read_only=True)

    avg_mark = serializers.FloatField(source='get_average_mark', read_only=True)

    class Meta:
        model = Skill
        read_only_fields = ('user', )
