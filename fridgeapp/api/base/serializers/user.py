from rest_framework import serializers

from fridgeapp.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="id")

    class Meta:
        model = CustomUser
        fields = ("user_id", "username")
