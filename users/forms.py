from django import forms

from candf.constants import EMAIL_ERROR
from candf.mixins import GitHubURLMixin
from users.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["name", "surname", "email", "password"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(EMAIL_ERROR)
        return email


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class EditProfileForm(GitHubURLMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "surname", "avatar", "about", "phone", "github_url"]
        labels = {
            "name": "Имя",
            "surname": "Фамилия",
            "about": "Обо мне",
            "phone": "Номер телефона",
            "github_url": "Ссылка на профиль GitHub",
        }
        widgets = {
            "avatar": forms.FileInput(),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone:
            return phone
        if (len(phone) not in (11, 12)) or (not phone[1:].isdigit()):
            raise forms.ValidationError("Некорректный номер телефона")
        if phone[0] == "8" and len(phone) == 11:
            phone = "+7" + phone[1:]
        elif phone[0] + phone[1] == "+7" and len(phone) == 12:
            pass
        else:
            raise forms.ValidationError(
                "Введите номер телефона в формате 8XXXXXXXXXX или +7XXXXXXXXXX"
            )
        if User.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError("Этот номер телефона уже используется")
        return phone


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)
    new_password2 = forms.CharField(
        label="Повторите пароль", widget=forms.PasswordInput
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Неверно введён текущий пароль")
        return old_password

    def clean(self):
        cleaned = super().clean()
        new_password1 = cleaned.get("new_password1")
        new_password2 = cleaned.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Пароли не совпадают")
        if self.user and new_password1 and self.user.check_password(new_password1):
            raise forms.ValidationError("Новый пароль должен отличаться от старого")
        return cleaned
