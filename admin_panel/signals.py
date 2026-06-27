from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import escape

from accounts.models import OrganizerApplication
from .models import ActivityLog
from events.models import Event


def get_display_name(user):
    """
    Helper function to safely extract the user's name.
    Falls back to the email address if full_name is empty.
    """
    # Check if profile exists (handles edge cases where profile isn't created yet)
    if hasattr(user, 'profile') and user.profile.full_name.strip():
        return escape(user.profile.full_name)
    return escape(user.email)


@receiver(post_save, sender=OrganizerApplication)
def log_organizer_application_activity(sender, instance, created, **kwargs):
    user_name = get_display_name(instance.user)
    organization_name = escape(instance.organization_name)

    if created:
        ActivityLog.objects.create(
            dot_color='var(--amber)',
            html_text=f'<span class="feed-actor">{user_name}</span> submitted an organizer application for <strong>{organization_name}</strong>'
        )
    elif hasattr(instance, 'status'):
        if instance.status == 'APPROVED':
            ActivityLog.objects.create(
                dot_color='var(--green)',
                html_text=f'Application for <strong>{organization_name}</strong> was <span style="color:var(--green);font-weight:600">approved</span>'
            )
        elif instance.status == 'REJECTED':
            reason = escape(getattr(instance, 'rejection_reason', 'Incomplete documents'))
            ActivityLog.objects.create(
                dot_color='var(--red)',
                html_text=f'Application for <strong>{organization_name}</strong> was <span style="color:var(--red);font-weight:600">rejected</span> — {reason}'
            )

@receiver(post_save, sender=Event)
def log_new_event(sender, instance, created, **kwargs):
    if created:
        creator_name =  get_display_name(instance.organizer.user)
        event_title = escape(instance.title)
        capacity = instance.capacity  # Integer fields don't need escaping

        ActivityLog.objects.create(
            dot_color='var(--blue)',
            html_text=f'<span class="feed-actor">{creator_name}</span> created event <strong>{event_title}</strong> · {capacity} capacity'
        )