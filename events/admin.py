from django.contrib import admin
from .models import Event,Ticket,TicketType

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title','organizer','start_time','end_time','venue','status')
    list_filter = ('status','start_time')
    search_fields = ('title','venue','description')
    list_editable = ('status',)
    


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id','event','user','ticket_type','quantity','payment_status')
    list_filter = ('unique_code','user__email','event__title')
    ordering = ['-created_at']


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('name','event','price','quantity_available')
