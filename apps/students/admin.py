from django.contrib import admin
from . models import Student
from unfold.admin import ModelAdmin

@admin.register(Student)
class CustomAdminClass(ModelAdmin):
    pass

