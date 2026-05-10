import os
from io import BytesIO

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from candf.constants import (
    USER_ABOUT_MAX_LENGTH,
    USER_AVATAR_COLORS,
    USER_AVATAR_FONT_PATH,
    USER_AVATAR_FONT_SIZE,
    USER_AVATAR_SIZE,
    USER_NAME_MAX_LENGTH,
    USER_PHONE_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
)


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, phone, password=None):
        if not email:
            raise ValueError("Email обязателен")
        if not name:
            raise ValueError("Имя обязательно")
        if not surname:
            raise ValueError("Фамилия обязательна")
        if not phone:
            raise ValueError("Номер телефона обязателен")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            surname=surname,
            phone=phone,
            is_active=True,
            is_staff=False,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, phone, password=None):
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            surname=surname,
            phone=phone,
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=USER_NAME_MAX_LENGTH, verbose_name="Имя")
    surname = models.CharField(
        max_length=USER_SURNAME_MAX_LENGTH, verbose_name="Фамилия"
    )
    avatar = models.ImageField(upload_to="avatars/", verbose_name="Аватар")
    phone = models.CharField(max_length=USER_PHONE_MAX_LENGTH, verbose_name="Телефон")
    github_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на GitHub")
    about = models.TextField(
        max_length=USER_ABOUT_MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name="Описание профиля",
    )
    is_active = models.BooleanField(default=True, verbose_name="Активный пользователь")
    is_staff = models.BooleanField(default=False, verbose_name="Администратор")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname", "phone"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["name", "surname"]

    def __str__(self):
        return self.email

    def generate_avatar(self):
        first_letter = self.name[0].upper() if self.name else "?"
        colors = USER_AVATAR_COLORS
        color_index = hash(self.email) % len(colors)
        bg_color = colors[color_index]
        image = Image.new("RGB", USER_AVATAR_SIZE, color=bg_color)
        draw = ImageDraw.Draw(image)
        font_path = os.path.join(
            settings.BASE_DIR, "static", "fonts", USER_AVATAR_FONT_PATH
        )
        try:
            font = ImageFont.truetype(font_path, USER_AVATAR_FONT_SIZE)
        except:
            font = ImageFont.load_default()

        try:
            bbox = draw.textbbox((0, 0), first_letter, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except:
            text_width, text_height = draw.textsize(first_letter, font=font)

        x = (USER_AVATAR_SIZE[0] - text_width) // 2
        y = (USER_AVATAR_SIZE[1] - text_height) // 2

        draw.text((x, y), first_letter, fill="#FFFFFF", font=font)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        safe_email = self.email.split("@")[0]
        filename = f"avatar_{safe_email}.png"
        self.avatar.save(filename, ContentFile(buffer.read()), save=False)
        buffer.close()

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.generate_avatar()
        super().save(*args, **kwargs)
