from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from local_extentions.utils import jalali_converter
from .managers import NotExpiredManager


User = get_user_model()


class UserLogin(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="logins", verbose_name=_("user") # handle on_delete in db level
    )
    refresh_token = models.CharField(max_length=600, verbose_name=_("refresh token"))
    expired_at = models.DateTimeField(verbose_name=_("expired time"))
    device_name = models.CharField(max_length=128, verbose_name=_("device name"))
    ip_address = models.GenericIPAddressField(verbose_name=_("ip address"))
    last_login = models.DateTimeField(verbose_name=_("last login"))

    default_manager = models.Manager()
    objects = NotExpiredManager()

    class Meta:
        verbose_name = _("user login")
        verbose_name_plural = _("users login")

    def __str__(self):
        return f"{self.user} - {self.device_name} - {self.ip_address}"

    def jlast_login(self):
        return jalali_converter(self.last_login)

    jlast_login.short_description = _("last login")
