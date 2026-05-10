from django.contrib.auth import get_user_model
from django.db import models

from candf.constants import (
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_STATUS_MAX_LENGTH,
    SKILL_NAME_MAX_LENGTH,
    STATUS_CHOICES,
    STATUS_OPEN,
)

User = get_user_model()


class Skill(models.Model):
    name = models.CharField(
        max_length=SKILL_NAME_MAX_LENGTH, unique=True, verbose_name="Название навыка"
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(
        max_length=PROJECT_NAME_MAX_LENGTH, verbose_name="Название проекта"
    )
    description = models.TextField(blank=True, verbose_name="Описание проекта")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Автор проекта",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    github_url = models.URLField(blank=True, verbose_name="Ссылка на GitHub")
    status = models.CharField(
        max_length=PROJECT_STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
        verbose_name="Статус проекта",
    )
    participants = models.ManyToManyField(
        User,
        blank=True,
        related_name="participated_projects",
        verbose_name="Участники проекта",
    )
    skills = models.ManyToManyField(
        Skill, blank=True, related_name="projects", verbose_name="Навыки"
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
