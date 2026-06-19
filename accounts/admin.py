from django.contrib import admin
from .models import User, UserProfile, OrganizerApplication
# Register your models here.

admin.site.register(User)
admin.site.register(UserProfile)





@admin.register(OrganizerApplication)
class OrganizerApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "organization_name", "status", "created_at")
    list_filter = ("status",)

    actions = ["approve_applications", "reject_applications"]

    def approve_applications(self, request, queryset):
        for app in queryset:
            app.approve()

    def reject_applications(self, request, queryset):
        for app in queryset:
            app.reject()