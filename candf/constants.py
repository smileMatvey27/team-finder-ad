# projects/models
SKILL_NAME_MAX_LENGTH = 124
# projects/models
PROJECT_NAME_MAX_LENGTH = 200
PROJECT_STATUS_MAX_LENGTH = 6
STATUS_OPEN = "open"
STATUS_CLOSED = "closed"
STATUS_CHOICES = [
    (STATUS_OPEN, "Открыт"),
    (STATUS_CLOSED, "Закрыт"),
]
# projects/views
PROJECTS_PAGINATE = 12
SKILL_SEARCH_LIMITATION = 10
# users/views
EMAIL_ERROR = "Такой email уже существует"
LOGIN_ERROR = "Неверный email или пароль"
# users/models
USER_NAME_MAX_LENGTH = 124
USER_SURNAME_MAX_LENGTH = 124
USER_PHONE_MAX_LENGTH = 12
USER_ABOUT_MAX_LENGTH = 256
USER_AVATAR_COLORS = [
    "#4A90E2",
    "#50E3C2",
    "#B8E986",
    "#F5A623",
    "#D0021B",
    "#9013FE",
    "#417505",
    "#8B572A",
    "#E94E77",
    "#4A4A4A",
]
USER_AVATAR_SIZE = (200, 200)
USER_AVATAR_FONT_SIZE = 120
USER_AVATAR_FONT_PATH = "Neue_Haas_Grotesk_Display_Pro_75_Bold.otf"
# candf/functions
PAGINATOR_FOR_PAGE = 12
GIT_DOMAIN = "github.com"
GIT_URL_ERROR = "Введите URL."
