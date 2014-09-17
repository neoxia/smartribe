from rest_framework import serializers
from core.models import SkillCategory, Skill


class SkillCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SkillCategory
        fields = ('url', 'name', 'detail')


class SkillCreateSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField()
    category = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Skill
        fields = ('url', 'user', 'category', 'description')


class SkillSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField()
    category = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Skill
        fields = ('url', 'user', 'category', 'description')
        read_only_fields = ('user',)
