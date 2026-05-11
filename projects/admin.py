from django.contrib import admin

from projects.models import Project, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "status",
        "skills_list",
        "participants_count",
        "created_at",
    )
    list_editable = ("status",)
    search_fields = ("name", "owner__email", "owner__name", "owner__surname")
    list_filter = ("status", "skills")

    @admin.display(description="Участники")
    def participants_count(self, obj):
        return obj.participants.count()

    @admin.display(description="Навыки")
    def skills_list(self, obj):
        return ", ".join([skill.name for skill in obj.skills.all()]) or "—"
