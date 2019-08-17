from rest_framework import serializers

from sunflower.models.cookbook import CookBook


class SubCookBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = CookBook
        fields = ('cookbook_id', 'name')


class CookBookSerializer(serializers.ModelSerializer):
    cookbook_id = serializers.IntegerField(source='pk', required=False)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CookBook
        fields = ('cookbook_id', 'name', 'author')
