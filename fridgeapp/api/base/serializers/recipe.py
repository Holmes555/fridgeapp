from rest_framework import serializers

from fridgeapp.api.base.serializers.ingredient import IngredientSerializer
from fridgeapp.api.base.serializers.recipe_step import RecipeStepSerializer
from fridgeapp.api.base.serializers.user import UserSerializer
from fridgeapp.models.recipe import Recipe
from fridgeapp.models.recipe_rating import RecipeRating
from fridgeapp.services.service.recipe_rating import RecipeRatingService


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    recipe_id = serializers.IntegerField(source="pk", required=False)
    author = UserSerializer(default=serializers.CurrentUserDefault())

    ingredients = IngredientSerializer(many=True, required=True)
    recipe_steps = RecipeStepSerializer(many=True, required=True)

    class Meta:
        model = Recipe
        fields = (
            "recipe_id",
            "title",
            "description",
            "photo",
            "cooking_time",
            "person_count",
            "author",
            "ingredients",
            "recipe_steps",
        )
        read_only_fields = ("publish_date",)

    def create(self, validated_data):
        rating = RecipeRating()
        added_rating = RecipeRatingService.add(rating)

        ingredients_data = validated_data.pop("ingredients")
        recipe_steps_data = validated_data.pop("recipe_steps")

        recipe = Recipe.objects.create(rating=added_rating, **validated_data)

        for ingredient in ingredients_data:
            serializer = IngredientSerializer()
            ingredient = serializer.create(ingredient)
            recipe.ingredients.add(ingredient)

        for recipe_step in recipe_steps_data:
            serializer = RecipeStepSerializer()
            recipe_step = serializer.create(recipe_step)
            recipe.recipe_steps.add(recipe_step)

        return recipe


class RecipeGetSerializer(serializers.ModelSerializer):
    recipe_id = serializers.IntegerField(source="pk")
    publish_date = serializers.DateField(format="%Y-%m-%d")

    author = UserSerializer(default=serializers.CurrentUserDefault())
    rating = serializers.CharField(source="rating.rating", default=0, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "recipe_id",
            "title",
            "description",
            "photo",
            "publish_date",
            "cooking_time",
            "person_count",
            "rating",
            "author",
        )
        read_only_fields = ("publish_date",)
