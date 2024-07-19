# Home/serializers.py

from rest_framework import serializers
from .models import RssUrls, RssData, RssSkills, SkillsJunction


class RssUrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RssUrls
        fields = '__all__'


class RssDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RssData
        fields = '__all__'


class RssSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RssSkills
        fields = '__all__'


class SkillsJunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillsJunction
        fields = '__all__'
