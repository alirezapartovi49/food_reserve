from datetime import timedelta, datetime

from django.contrib import admin
from django.forms import ModelForm, SelectMultiple
from django_jalali.admin.filters import JDateFieldListFilter

from .models import FoodDate, Food, PredefinedFood, SideFishes

from local_extentions.utils import jalali_date_converter


class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = "__all__"
        widgets = {
            "side_fishes": SelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.predefined_food:
            self.fields["custom_name"].disabled = True
            self.fields["food_type"].disabled = True
            self.fields["description"].disabled = True

        if self.instance.pk and self.instance.food_type:
            self.fields["side_fishes"].queryset = SideFishes.objects.filter(
                foods__food_type=self.instance.food_type
            ).distinct()


class FoodInline(admin.TabularInline):
    model = Food
    extra = 2
    max_num = 2
    min_num = 2
    form = FoodForm
    verbose_name_plural = "غذاهای این تاریخ"
    autocomplete_fields = ["predefined_food", "side_fishes"]
    filter_horizontal = ["side_fishes"]


@admin.register(PredefinedFood)
class PredefinedFoodAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "food_type", "description", "used_count"]

    def used_count(self, obj: PredefinedFood):
        past_days = datetime.now() - timedelta(days=30)
        return str(obj.food_set.filter(food_date__date__gte=past_days).count())

    used_count.short_description = "تعداد استفاده در ماه اخیر"


@admin.register(FoodDate)
class FoodDateAdmin(admin.ModelAdmin):
    inlines = [FoodInline]
    list_display = ("jdate", "day_foods")
    list_filter = (("date", JDateFieldListFilter),)

    def day_foods(self, obj):
        return " - ".join(
            [str(food) for food in obj.food_set.all().only("custom_name")]
        )

    def jdate(self, obj):
        return jalali_date_converter(obj.date)

    day_foods.short_description = "غذاهای روز"
    jdate.short_description = "تاریخ"


@admin.register(SideFishes)
class SideFishesAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "used_count",
        "food_list",
    )
    search_fields = ["name"]
    filter_horizontal = ["foods"]
    list_per_page = 20
    list_filter = ("is_active",)

    def used_count(self, obj: SideFishes):
        return str(obj.foods.count())

    def food_list(self, obj):
        return ", ".join([food.name for food in obj.foods.all()])

    food_list.short_description = "Associated Foods"
    used_count.short_description = "تعداد استفاده شده"
