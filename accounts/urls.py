from django.urls import path

from .views import edit_user_profile, apply_organizer

app_name = 'accounts'

urlpatterns = [
    path('edit-profile/', edit_user_profile,name='edit_profile'),
    path('onboarding/', edit_user_profile,name='profile_onboarding'),
    path('apply-organizer/', apply_organizer,name='apply_organizer'),
]
