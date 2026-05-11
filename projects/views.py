import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from candf.constants import SKILL_SEARCH_LIMITATION, STATUS_CLOSED, STATUS_OPEN
from candf.functions import paginate_queryset
from projects.forms import ProjectForm
from projects.models import Project, Skill


def project_list(request):
    skill_name = request.GET.get("skill")
    skills = Skill.objects.values_list("name", flat=True)
    projects = (
        Project.objects.select_related("owner")
        .prefetch_related("skills", "participants")
        .order_by("-created_at")
    )
    skill_now = None
    if skill_name:
        projects = projects.filter(skills__name=skill_name).distinct()
        skill_now = skill_name
    page = paginate_queryset(request, projects)
    return render(
        request,
        "projects/project_list.html",
        {
            "projects": page,
            "all_skills": skills,
            "active_skill": skill_now,
        },
    )


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, "projects/project-details.html", {"project": project})


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect("projects:project_detail", project_id=project.id)
    return render(
        request, "projects/create-project.html", {"form": form, "is_edit": False}
    )


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if project.owner != request.user:
        return redirect("projects:project_list")
    if form.is_valid():
        form.save()
        return redirect("projects:project_detail", project_id=project.id)
    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": True},
    )


@login_required
def complete_project(request, project_id):
    if request.method != "POST":
        return JsonResponse({"status": "error"})
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user:
        return JsonResponse({"status": "error"})
    if project.status != STATUS_OPEN:
        return JsonResponse({"status": "error"})
    project.status = STATUS_CLOSED
    project.save()
    return JsonResponse({"status": "ok", "project_status": STATUS_CLOSED})


@login_required
def toggle_participate(request, project_id):
    if request.method != "POST":
        return JsonResponse({"status": "error"})
    project = get_object_or_404(Project, id=project_id)
    if project.participants.filter(id=request.user.id).exists():
        project.participants.remove(request.user)
        return JsonResponse({"status": "ok", "participant": False})
    project.participants.add(request.user)
    return JsonResponse({"status": "ok", "participant": True})


def skill_search(request):
    query_of_skills = request.GET.get("q", "").strip()
    skills = Skill.objects.filter(name__istartswith=query_of_skills).order_by("name")[
        :SKILL_SEARCH_LIMITATION
    ]
    sk_data = list(skills.values("id", "name"))
    return JsonResponse(sk_data, safe=False)


@login_required
def skills_add(request, project_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"})

    project = get_object_or_404(Project, id=project_id)

    if project.owner != request.user:
        return JsonResponse({"error": "Нет доступа"})

    data = json.loads(request.body)
    skill_id = data.get("skill_id")
    name = data.get("name")

    created = False
    added = False

    if skill_id:
        skill = get_object_or_404(Skill, id=skill_id)
    elif name:
        name = name.strip()
        skill, created = Skill.objects.get_or_create(name=name)
    else:
        return JsonResponse({"error": "Нет данных"})

    if not project.skills.filter(id=skill.id).exists():
        project.skills.add(skill)
        added = True

    return JsonResponse(
        {"id": skill.id, "name": skill.name, "created": created, "added": added}
    )


@login_required
def remove_skill(request, project_id, skill_id):
    if request.method != "POST":
        return JsonResponse({"status": "error"})
    project = get_object_or_404(Project, id=project_id)
    skill = get_object_or_404(Skill, id=skill_id)
    if project.owner != request.user:
        return JsonResponse({"error": "У вас нет прав для выполнения этого действия"})
    if project.skills.filter(id=skill.id).exists():
        project.skills.remove(skill)
    return JsonResponse({"removed": True})
