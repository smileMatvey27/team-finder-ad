from django import forms

from candf.functions import validate_url_for_gh
from projects.models import Project


class ProjectForm(forms.ModelForm):
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

    def clean_github_url(self):
        url = self.cleaned_data.get("github_url")
        return validate_url_for_gh(url)
