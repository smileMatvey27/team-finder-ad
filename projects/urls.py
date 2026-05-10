from django.urls import path

from projects import views

app_name = "projects"

urlpatterns = [
    path("list/", views.project_list, name="project_list"),
    path("<int:project_id>/", views.project_detail, name="project_detail"),
    path("create-project/", views.create_project, name="create_project"),
    path("<int:project_id>/edit/", views.edit_project, name="edit_project"),
    path("<int:project_id>/complete/", views.complete_project, name="complete_project"),
    path(
        "<int:project_id>/toggle-participate/",
        views.toggle_participate,
        name="toggle_participate",
    ),
    path("skills/", views.skill_search, name="skill_search"),
    path("<int:project_id>/skills/add/", views.skills_add, name="add_skill"),
    path(
        "<int:project_id>/skills/<int:skill_id>/remove/",
        views.remove_skill,
        name="remove_skill",
    ),
]
