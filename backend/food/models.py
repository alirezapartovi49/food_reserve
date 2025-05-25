from django.core.exceptions import ValidationError
from django.db import models


class FoodTypeChoices(models.TextChoices):
    POLO = "pl", "پلو"
    BREAD = "br", "نونی"


class SideFishes(models.Model):
    name = models.CharField(verbose_name="نام", max_length=30)
    foods = models.ManyToManyField("PredefinedFood", verbose_name="عذا ها")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "ویژگی اضافه"
        verbose_name_plural = "ویژگی های اضافه"

    def __str__(self) -> str:
        return "ویژگی " + self.name


class PredefinedFood(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="نام غذا",
        unique=True,
    )
    food_type = models.CharField(
        max_length=2, choices=FoodTypeChoices.choices, verbose_name="نوع غذا"
    )
    description = models.TextField(blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "غذای پیش تعریف شده"
        verbose_name_plural = "غذاهای از پیش تعریف شده"

    def __str__(self):
        return self.name


class FoodDate(models.Model):
    date = models.DateField(unique=True, verbose_name="تاریخ")

    class Meta:
        verbose_name = "غذای تاریخ"
        verbose_name_plural = "غذاها براساس تاریخ"

    def __str__(self):
        return str(self.date)


class Food(models.Model):
    food_date = models.ForeignKey(
        FoodDate, on_delete=models.CASCADE, verbose_name="تاریخ"
    )
    predefined_food = models.ForeignKey(
        PredefinedFood,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="انتخاب غذای پیش‌فرض",
    )
    custom_name = models.CharField(
        max_length=100, blank=True, verbose_name="نام غذا (سفارشی)"
    )
    food_type = models.CharField(
        max_length=2,
        choices=FoodTypeChoices.choices,
        default=FoodTypeChoices.POLO,
        verbose_name="نوع غذا",
    )
    side_fishes = models.ManyToManyField(
        SideFishes, blank=True, verbose_name="ویژگی های اضافه"
    )
    description = models.TextField(blank=True, verbose_name="توضیحات")

    def clean(self):
        if not self.predefined_food and not self.custom_name:
            raise ValidationError(
                "یا غذای پیش‌فرض انتخاب کنید یا نام غذا را وارد نمایید."
            )

    def save(self, *args, **kwargs):
        if self.custom_name and not self.predefined_food:
            predefined_food, created = PredefinedFood.objects.get_or_create(
                name=self.custom_name,
                defaults={"food_type": self.food_type, "description": self.description},
            )
            self.predefined_food = predefined_food
            self.custom_name = ""
        super().save(*args, **kwargs)

    def __str__(self):
        return self.predefined_food.name if self.predefined_food else self.custom_name
