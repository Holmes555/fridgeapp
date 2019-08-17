from rest_framework import serializers

from sunflower.models.tag import Tag


class TagSerializer(serializers.ModelSerializer):
    tag_id = serializers.IntegerField(source='pk', required=False)

    class Meta:
        model = Tag
        fields = ('tag_id', 'title', 'popularity')
