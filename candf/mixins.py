from candf.functions import validate_url_for_gh


class GitHubURLMixin:
    def clean_github_url(self):
        url = self.cleaned_data.get("github_url")
        return validate_url_for_gh(url)
