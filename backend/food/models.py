from django.db import models


class FoodTypeChoices(models.TextChoices):
    POLO = "pl", "پلو"
    BREAD = "br", "نونی"


class FoodDate(models.Model):
    date = models.DateField(unique=True, verbose_name="تاریخ")

    class Meta:
        verbose_name = "غذای تاریخ"
        verbose_name_plural = "غذا ها براساس تاریخ"

    def __str__(self):
        return str(self.date)


class Food(models.Model):
    food_date = models.ForeignKey(
        FoodDate, on_delete=models.CASCADE, verbose_name="تاریخ"
    )
    name = models.CharField(max_length=100, verbose_name="نام غذا")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    food_type = models.CharField(
        choices=FoodTypeChoices.choices,
        default=FoodTypeChoices.POLO,
    )

    class Meta:
        verbose_name = "غذا"
        verbose_name_plural = "غذاها"
        constraints = [
            models.UniqueConstraint(
                fields=["food_date", "name"], name="unique_food_per_date"
            )
        ]

    def __str__(self):
        return self.name
