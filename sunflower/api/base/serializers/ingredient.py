from rest_framework import serializers

from sunflower.models.ingredient import Ingredient
from sunflower.services.service.ingredient import IngredientService
from sunflower.services.service.product import ProductService


class IngredientSerializer(serializers.ModelSerializer):
    ingredient_id = serializers.IntegerField(source='pk', required=False)

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.CharField(source='product.name', default='',
                                    max_length=100)

    class Meta:
        model = Ingredient
        fields = ('ingredient_id', 'quantity', 'measure', 'product',
                  'author')

    def create(self, validated_data):
        kwargs = validated_data.pop("product")
        product, _ = ProductService.get_or_create(kwargs)
        ingredient = Ingredient(product=product, **validated_data)
        return IngredientService.add(ingredient)
