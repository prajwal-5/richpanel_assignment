from atexit import register
from django.contrib import admin
from .models import User, Plan

# Register your models here.
@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'password', 'plan_period', 'is_loggedin']


@admin.register(Plan)
class PlanModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'monthly_price', 'yearly_price', 'video_quality', 'resolution', 'devices', 'active_screens', 'user']