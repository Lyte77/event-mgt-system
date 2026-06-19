# admin_panel/views.py
from multiprocessing import context
from django.shortcuts import render
from accounts.models import User
from admin_panel.models import ActivityLog
from events.models import Event
from accounts.models import OrganizerApplication
from django.utils import timezone
from .decorators import admin_required



@admin_required
def dashboard(request):
    total_users = User.objects.count()
    active_organizers = User.objects.filter(profile__is_organizer=True).count()
    pending_apps = OrganizerApplication.objects.filter(status="pending").count()
    total_events = Event.objects.count()

    context = {
        "total_users": total_users,
        "active_organizers": active_organizers,
        "pending_applications": pending_apps,
        "total_events": total_events,
    }
        
    if request.htmx:
        return render(request, "admin_panel/dashboard/overview_partial.html", context)
    return render(request, "admin_panel/dashboard/overview.html", context)


def kpi_cards(request):
    context = {
        "total_users": User.objects.count(),
        "active_organizers": User.objects.filter(
            profile__is_organizer=True
        ).count(),
        "pending_applications": OrganizerApplication.objects.filter(
            status="pending"
        ).count(),
        "total_events": Event.objects.count(),

        # placeholders for now
        "tickets_issued": 0,
        "todays_checkins": 0,
    }

    return render(
        request,
        "admin_panel/partials/kpi_cards.html",
        context
    )

def applicant_poll(request):
    pending_count = OrganizerApplication.objects.filter(status="pending").count()
    oldest_application = OrganizerApplication.objects.filter(
    status="pending"
).order_by("created_at").first()
    oldest_age_days = None

    if oldest_application:
        oldest_age_days = (timezone.now() - oldest_application.created_at).days
    return render(request, "admin_panel/partials/applicant_poll.html", {"pending_count": pending_count,
                                                                        "oldest_day_age":oldest_age_days})


def activity_feed_items(request):
    """
    Returns only the HTML fragments for the active activity feed.
    Polled directly by HTMX.
    """
    # Fetch the 10 most recent log entries
    logs = ActivityLog.objects.all()[:10]


    return render(request, 'admin_panel/partials/feed_items.html', {'logs': logs})

def pending_applicants(request):
    pending_count = OrganizerApplication.objects.filter(status="pending")
    oldest_application = OrganizerApplication.objects.filter(
    status="pending"
).order_by("created_at").first()
    oldest_age_days = None

    if oldest_application:
        oldest_age_days = (timezone.now() - oldest_application.created_at).days
    return render(request, "admin_panel/partials/pending_applicants.html", {"pending_count": pending_count,
                                                                        "oldest_day_age":oldest_age_days})

def alert_notification_banner(request):
    pending_count = OrganizerApplication.objects.filter(status="pending").count()
    oldest_application = OrganizerApplication.objects.filter(
    status="pending"
).order_by("created_at").first()
    oldest_age_days = None

    if oldest_application:
        oldest_age_days = (timezone.now() - oldest_application.created_at).days
    return render(request, "admin_panel/partials/alert_notifications.html", {"pending_count": pending_count,

                                                                    "oldest_day_age":oldest_age_days})

def applications(request):
    apps = OrganizerApplication.objects.select_related("user").all().order_by("-created_at")
    if request.htmx :
        return render(request, "admin_panel/applications/table.html", {"applications": apps})
    return render(request, 'admin_panel/applications/list.html', {"applications": apps})


def users(request):
    users = User.objects.select_related("profile").all()
    if request.htmx:
        return render(request, "admin_panel/users/table.html", {"users": users})
    return render(request, 'admin_panel/users/list.html', {"users": users})

def events(request):
    events = Event.objects.select_related("organizer").all()
    if request.htmx:
        return render(request, "admin_panel/events/table.html", {"events": events})
    return render(request, 'admin_panel/events/list.html', {"events": events})



def approve_application(request, pk):
    app = OrganizerApplication.objects.get(pk=pk)
    app.approve()

    return render(request, "admin_panel/partials/application_row.html", {
        "app": app
    })

def reject_application(request, pk):
    app = OrganizerApplication.objects.get(pk=pk)
    app.reject()

    return render(request, "admin/partials/application_row.html", {
        "app": app
    })