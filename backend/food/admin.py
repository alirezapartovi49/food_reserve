from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet, ModelForm
from django.contrib import admin

from django_jalali.admin.filters import JDateFieldListFilter

from .models import FoodDate, Food
from local_extentions.utils import jalali_date_converter


class FoodDateForm(ModelForm):
    class Meta:
        model = FoodDate
        fields = "__all__"


class CustomInlineFormset(BaseInlineFormSet):
    def clean(self):
        self.validate_unique()

        if self.is_valid():
            if len(self.forms) != 2:
                raise ValidationError("برای هر تاریخ باید دقیقاً دو غذا تعریف شود.")


class FoodInline(admin.TabularInline):
    model = Food
    extra = 2
    max_num = 2
    min_num = 2
    # can_delete = False

    verbose_name_plural = "غذاهای این تاریخ"
    formset = CustomInlineFormset


@admin.register(FoodDate)
class FoodDateAdmin(admin.ModelAdmin):
    inlines = [FoodInline]
    form = FoodDateForm
    list_display = (
        "jdate",
        "day_foods",
    )
    list_filter = (("date", JDateFieldListFilter),)

    def day_foods(self, obj: FoodDate):
        foods = obj.food_set.all().only("name")
        food_names = [food.name for food in foods]
        return " - ".join(food_names) if food_names else "-"

    def jdate(self, obj: FoodDate):
        return jalali_date_converter(obj.date)

    day_foods.short_description = "غذاهای روز"
    jdate.short_description = "تاریخ"
