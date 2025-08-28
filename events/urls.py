from django.urls import path
from . import views


app_name = 'events'

urlpatterns = [
    path('',views.homepage,name='home'),
    path('dashboard/', views.organizer_dashboard,name='dashboard'),
    path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
    path('profile/',views.profile,name='profile'),
    path('redirect/', views.redirect_after_login,name='redirect_after_login'),

    path('all-events', views.event_list,name='event_list'),
    path('create-event/', views.create_event, name='create_event'),
    path('<slug:slug>/', views.event_detail,name='event_detail'),
    path('update_event/<slug:slug>/',views.event_update,name='update_event'),
    path('delete-event/<slug:slug>/',views.delete_event,name='delete_event'),

    path('<uuid:event_id>/ticket/<int:ticket_type_id>/purchase/',views.purchase_ticket,name='purchase_ticket')
]
