from datetime import datetime, date

from rest_framework import serializers

from local_extentions.utils import jalali_date_converter
from reserve.models import Reserve
from accounts.models import User
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
    user_reserved_ids: list = serializers.SerializerMethodField(
        method_name="get_reserved"
    )
    can_reserve: bool = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.FoodDate
        fields = "__all__"

    def get_jdate(self, obj: models.FoodDate) -> str:
        return jalali_date_converter(obj.date)

    def get_reserved(self, obj: models.FoodDate) -> list[int] | list[None]:
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            print("user or request does not exists")
            return []

        request_user = request.user
        reserves = Reserve.objects.filter(user=request_user, date=obj.date)
        food_ids = list(reserves.values_list("food__id", flat=True))

        return food_ids

    def get_can_reserve(self, obj: models.FoodDate):
        print(str(date.today()) + str(obj.date))
        return True if date.today() < obj.date else False

    # def get_foods(self, obj):
    #     return FoodSerializer(food for food in obj.food_set.all()).data
