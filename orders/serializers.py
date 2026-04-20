from rest_framework import serializers
from . import models




class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderItem
        fields = '__all__'