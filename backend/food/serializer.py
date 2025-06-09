from datetime import date

from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

from local_extentions.utils import jalali_date_converter
from . import models


class SideFishesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SideFishes
        fields = "__all__"


class PredefinedFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PredefinedFood
        fields = "__all__"


class FoodSerializer(serializers.ModelSerializer):
    side_fishes = SideFishesSerializer(many=True, read_only=True)
    predefined_food = PredefinedFoodSerializer(read_only=True)

    class Meta:
        model = models.Food
        fields = "__all__"


class FoodDateSerializer(serializers.ModelSerializer):
    foods = FoodSerializer(many=True, read_only=True, source="food_set")
    jdate: str = serializers.SerializerMethodField()
    can_reserve: bool = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.FoodDate
        fields = "__all__"

    def get_jdate(self, obj: models.FoodDate) -> str:
        return jalali_date_converter(obj.date)

    @extend_schema_field(OpenApiTypes.STR)
    def get_can_reserve(self, obj: models.FoodDate):
        print(str(date.today()) + str(obj.date))
        return True if date.today() < obj.date else False
