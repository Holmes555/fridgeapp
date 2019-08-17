from rest_framework import serializers

from fridgeapp.models.recipe_step import RecipeStep


class RecipeStepSerializer(serializers.ModelSerializer):
    recipe_step_id = serializers.IntegerField(source="pk", required=False)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = RecipeStep
        fields = ("recipe_step_id", "description", "photo", "author", "step_number")
