from django.apps import AppConfig


class FoodConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "food"
    verbose_name = "غذا"
    verbose_name_plural = "غذا ها"
