from django.contrib.auth.models import BaseUserManager


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
