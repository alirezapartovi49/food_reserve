from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    Permission,
    Group,
)

from local_extentions.utils import jalali_converter
from .managers import UserManager


class Self(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام سلف")
    code = models.CharField(max_length=20, unique=True, verbose_name="کد سلف")
    address = models.TextField(verbose_name="آدرس")
    is_active = models.BooleanField(verbose_name="فعال؟", default=True)

    class Meta:
        verbose_name = "سلف"
        verbose_name_plural = "سلف‌ ها"

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=120, unique=True, db_index=True, verbose_name="ایمیل"
    )
    fullname = models.CharField(max_length=34, verbose_name="نام کامل")
    city = models.CharField(verbose_name="شهر", default="tehran", max_length=100)
    username = models.CharField(max_length=20, unique=True, verbose_name="نام کاربری")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="فعال ؟")
    is_ban = models.BooleanField(
        default=False, db_index=True, verbose_name="محدود شده ؟"
    )
    is_admin = models.BooleanField(default=False, verbose_name="ادمین ؟")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    modified_at = models.DateTimeField(auto_now=True)
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="auth_user_set",
        related_query_name="user",
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name="گروه ها",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="auth_user_set",
        related_query_name="user",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("fullname",)

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        managed = True

    def __str__(self):
        return self.fullname

    def is_staff(self):
        return self.is_admin

    def jlast_login(self):
        return jalali_converter(self.last_login)

    def jcreated_at(self):
        return jalali_converter(self.created_at)

    jcreated_at.short_description = "زمان ساخت اکانت"
    jlast_login.short_description = "آخرین ورود"


class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.code}"


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="حساب کاربری"
    )
    university = models.ForeignKey(
        Self,
        on_delete=models.CASCADE,
        verbose_name="سلف",
        related_name="students",
        db_column="self",
    )
    student_id = models.CharField(max_length=20, verbose_name="شماره دانشجویی")
    has_dormitory = models.BooleanField(verbose_name="دارای خوابگاه")

    class Meta:
        verbose_name = "دانشجو"
        verbose_name_plural = "دانشجویان"

    def __str__(self):
        return f"{self.user.fullname} - {self.university.name}"
