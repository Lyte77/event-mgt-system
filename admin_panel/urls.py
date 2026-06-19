from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
   
    path("dashboard/", views.dashboard, name="dashboard"),
    path("applications/", views.applications, name="applications"),
    
    path("users/", views.users, name="users"),
    path("events/", views.events, name="events"),

    
    path("applications/<int:pk>/approve/", views.approve_application, name="approve_application"),
    path("applications/<int:pk>/reject/", views.reject_application, name="reject_application"),

    # partials for HTMX
    path("partials/kpis/", views.kpi_cards, name="kpi_cards"),
    path("partials/applicant_poll/", views.applicant_poll, name="applicant_poll"),
    path("partials/feed_items/", views.activity_feed_items, name="feed_items"),
    path("partials/pending_applicants/", views.pending_applicants, name="pending_applicants"),
    path("partials/alert_notifications/", views.alert_notification_banner, name="alert_notification_banner"),
]



