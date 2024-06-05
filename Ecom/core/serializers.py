from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('productID',
                  'category',
                  'size',
                  'name',
                  'price',
                  'price_discounted',
                  'stock',
                  'image',
                  'description')


