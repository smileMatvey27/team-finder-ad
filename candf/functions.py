from django.core.exceptions import ValidationError
from django.core.paginator import Paginator

from candf.constants import GIT_DOMAIN, GIT_URL_ERROR, PAGINATOR_FOR_PAGE


def paginate_queryset(request, queryset, per_page=PAGINATOR_FOR_PAGE):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def validate_url_for_gh(github_url):
    if github_url and GIT_DOMAIN not in github_url:
        raise ValidationError(GIT_URL_ERROR)
    return github_url
