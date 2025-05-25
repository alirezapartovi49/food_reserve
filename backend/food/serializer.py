from rest_framework import serializers

from . import models


class SideFishesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SideFishes
        fields = "__all__"


class FoodSerializer(serializers.ModelSerializer):
    side_fishes = SideFishesSerializer(many=True, read_only=True)

    class Meta:
        model = models.Food
        fields = "__all__"


class FoodDateSerializer(serializers.ModelSerializer):
    foods = FoodSerializer(many=True, read_only=True, source="food_set")

    class Meta:
        model = models.FoodDate
        fields = "__all__"

    # def get_foods(self, obj):
    #     return FoodSerializer(food for food in obj.food_set.all()).data
