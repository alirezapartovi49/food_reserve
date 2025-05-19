from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_("password"), widget=forms.PasswordInput())
    password2 = forms.CharField(label=_("repeat password"), widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("email", "fullname")

    def clean_password2(self):
        password1, password2 = self.cleaned_data.get(
            "password1"
        ), self.cleaned_data.get("password2")
        if password1 and password2 and password1 == password2:
            return password2
        raise forms.ValidationError(_("passwords don't match"))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='شما میتوانید پسورد خود را در این <a href="../password/">لینک</a> تغییر دهید'
    )

    class Meta:
        model = User
        fields = (
            "email",
            "fullname",
            "username",
            "is_active",
            "is_ban",
            "is_admin",
            "is_superuser",
        )
