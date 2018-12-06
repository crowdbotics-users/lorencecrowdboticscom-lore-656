from django.contrib import admin

from .models import (
    Category,
    Task,
    Todo,
    TodoImage,
    Application,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'customer', 'tasker', 'start_date', 'address',)


class TodoImageInline(admin.StackedInline):
    model = TodoImage
    extra = 1


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('task',)
    inlines = [TodoImageInline,]


@admin.register(TodoImage)
class TodoImageAdmin(admin.ModelAdmin):
    list_display = ('image',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('task', 'tasker',)
