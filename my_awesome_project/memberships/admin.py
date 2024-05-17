from django.contrib import admin

from .models import Membership
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name", "description", "created_at")


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("uuid", "user", "organization", "created_at")
