from django.contrib import admin

from local_extentions.utils import jalali_converter, jalali_date_converter
from .models import Reserve


@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "food",
        "jdate",
        "jcreated_at",
        "is_delivered",
    )
    list_filter = ("is_delivered",)

    def jcreated_at(self, obj: Reserve) -> str:
        return jalali_converter(obj.created_at)

    def jdate(self, obj: Reserve) -> str:
        return jalali_date_converter(obj.date)

    jcreated_at.short_description = "زمان رزرو"
    jdate.short_description = "تاریخ تحویل غذا"
