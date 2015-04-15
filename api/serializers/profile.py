from rest_framework import serializers
from api.serializers.skill import SkillSerializer
from core.models import Profile


class ProfileCreateSerializer(serializers.ModelSerializer):

    is_early_adopter = serializers.BooleanField(read_only=True)

    is_donor = serializers.BooleanField(read_only=True)

    title = serializers.CharField(max_length=255, source='get_title', read_only=True)

    level = serializers.FloatField(source='get_user_level', read_only=True)

    class Meta:
        model = Profile


class ProfileSerializer(serializers.ModelSerializer):

    is_early_adopter = serializers.BooleanField(read_only=True)

    is_donor = serializers.BooleanField(read_only=True)

    title = serializers.CharField(max_length=255, source='get_title', read_only=True)

    level = serializers.FloatField(source='get_user_level', read_only=True)

    skills = SkillSerializer(source='get_skills', many=True, read_only=True)

    class Meta:
        model = Profile
        read_only_fields = ('user', )
