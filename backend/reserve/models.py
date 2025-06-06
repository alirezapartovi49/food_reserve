from django.db import models

from accounts.models import User
from food.models import Food


class Reserve(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="کاربر")
    food = models.ForeignKey(
        Food, on_delete=models.PROTECT, verbose_name="غذای رزرو شده"
    )
    date = models.DateField(verbose_name="تاریخ غذای رزرو شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان رزرو")
    is_delivered = models.BooleanField(verbose_name="تحویل داده شده؟", default=False)

    def __str__(self) -> str:
        return str(self.user) + " - " + str(self.pk)

    class Meta:
        verbose_name = "رزرو"
        verbose_name_plural = "رزرو ها"
