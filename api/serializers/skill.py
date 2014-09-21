from rest_framework import serializers
from core.models import SkillCategory, Skill


class SkillCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SkillCategory


class SkillCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        read_only_fields = ('user', )
