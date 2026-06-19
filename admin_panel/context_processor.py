from accounts.models import OrganizerApplication

def admin_alerts(request):
    if not request.user.is_authenticated:
        return {}
    
    if not request.user.is_staff:
        return {}

    pending_apps = OrganizerApplication.objects.filter(
        status="Pending"
    ).count()

    return {
        "pending_apps": pending_apps
    }