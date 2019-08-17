from rest_framework import serializers

from sunflower.api.base.serializers.user import UserSerializer
from sunflower.models.recipe_comment import RecipeComment


class RecipeCommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField(source='pk', required=False)
    author = UserSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = RecipeComment
        fields = ('comment_id', 'content', 'photo', 'publish_date', 'author',
                  'recipe')
        read_only_fields = ('publish_date',)
