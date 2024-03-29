from rest_framework import serializers

from fridgeapp.models.product import Product


class ProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="pk", required=False)

    class Meta:
        model = Product
        fields = ("name",)
