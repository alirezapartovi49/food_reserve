from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from string import digits, ascii_letters, punctuation
from random import choices, randint


def generate_password(pattern: str = digits + ascii_letters + punctuation, k: int = 12):
    return "".join(choices(pattern, k=k))


def generate_username(email: str):
    email_x = email.split("@")[0]
    num = randint(1000, 9999)
    return f"{email_x}-{num}"


class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        fullname: str,
        password: str = generate_password(),
    ):
        if email is None:
            raise ValueError(_("User must have phone number"))
        elif password is None:
            raise ValueError(_("User must have password"))

        username = generate_username(email)

        user = self.model(email=email, fullname=fullname, username=username)
        if email:
            user.email = BaseUserManager.normalize_email(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(
        self,
        email: str,
        fullname: str,
        password: str = generate_password(),
    ):
        user = self.create_user(
            email=email,
            fullname=fullname,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        fullname: str,
        password: str = generate_password(),
    ):
        user = self.create_admin(
            email=email,
            fullname=fullname,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user
