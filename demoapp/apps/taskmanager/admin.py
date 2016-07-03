# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models


# Register your models here.
class ProjectsInLine(admin.TabularInline):
    model = models.Project
    extra = 5


class TagsInLine(admin.TabularInline):
    model = models.Tag
    extra = 0


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ("username", "interaction", "_projects", "_tags")

    search_fields = ["user__username"]

    inlines = [
        ProjectsInLine, TagsInLine,
    ]

    def _projects(self, obj):
        # obj is the Profile instance we're editing
        return obj.projects.all().count()

    def _tags(self, obj):
        return obj.tags.all().count()
