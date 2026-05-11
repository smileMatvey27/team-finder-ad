from django import forms

from candf.mixins import GitHubURLMixin
from projects.models import Project


class ProjectForm(GitHubURLMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Название проекта"}),
            "description": forms.Textarea(attrs={"placeholder": "Описание проекта"}),
            "github_url": forms.URLInput(
                attrs={"placeholder": "https://github.com/username/repo"}
            ),
        }
