from rest_framework import serializers
from api.serializers.skill import SkillSerializer
from core.models import Profile


class ProfileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile


class ProfileSerializer(serializers.ModelSerializer):

    skills = SkillSerializer(source='get_skills', many=True, read_only=True)

    class Meta:
        model = Profile
        read_only_fields = ('user', )
