from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.cache import cache

from django.utils.timezone import now
from django.http import HttpResponseForbidden
from .models import Event, TicketType, Ticket
from django.db.models import Sum, Count,Q
from .forms import EventForm,TicketTypeForm,TicketTypeFormSet
import uuid



# Create your views here.

def homepage(request):
    events = Event.objects.filter(is_published=True)[:4]
    upcoming_events = Event.objects.filter(status='upcoming')


    context = {'events':events,
               'upcoming_events': upcoming_events}
    return render(request, 'events/home.html',context)

def event_list(request):
    events = Event.objects.filter(is_published=True,status="upcoming")
    context = {'events':events}

    return render(request,'events/event_list.html',context)

def event_detail(request, slug):
    event = get_object_or_404(Event,slug=slug,is_published=True)
    ticket_type = TicketType.objects.filter(event=event)
    context = {'event':event,
               'ticket_type':ticket_type}
    return render(request, 'events/event_detail.html',context)


@login_required
def create_event(request):
    if not request.user.is_organizer:
        messages.error(request,"You must be an organizer to create events")
        return redirect('events:event_list')
    
    if request.method == 'POST':
        try:
            form = EventForm(request.POST, request.FILES)
            formset = TicketTypeFormSet(request.POST)
            if form.is_valid() and formset.is_valid():
                event = form.save(commit=False)
                event.organizer = request.user
                event.save()
                formset.instance = event
                formset.save()
                print("submitted")
                messages.success(request,"Event created successfully")
                return redirect('events:dashboard')
            else:
                print(form.errors)
                print(formset.errors)
        except:
            print("Cant submit form")
            
        # return redirect('events:event_detail',slug=event.slug)
    else:
        form = EventForm()
        formset = TicketTypeFormSet()
    context = {'form':form,
               'formset':formset}
    return render(request, 'events/create_event.html',context)

@login_required
def event_update(request,slug):
    event = get_object_or_404(Event,slug=slug,organizer=request.user)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES,instance=event)
        formset = TicketTypeFormSet(request.POST,instance=event)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('events:dashboard')
        else:
                print(form.errors)
                print(formset.errors)
    else:
        form = EventForm(instance=event)
        formset = TicketTypeFormSet(instance=event)
    context = {'form':form,
               'formset':formset }
    return render(request, 'events/create_event.html',context)


@login_required
def delete_event(request,slug):
    event = get_object_or_404(Event,slug=slug,organizer=request.user)
    event.delete()
    return redirect('events:dashboard')
        
    
    
def dashboard_router(request):
    if request.user.is_authenticated:
        if request.user.is_organizer:
            return redirect('events:dashboard')
        else:
            return redirect('events:user_dashboard')

@login_required
def organizer_dashboard(request):
    if not request.user.is_organizer:
        return redirect('events:home')
    
    organizer = request.user
    events = (
        Event.objects.filter(organizer=organizer)
        .annotate(
            total_tickets=Count("tickets"),
            paid_tickets=Count("tickets", filter=Q(tickets__payment_status="paid")),
            unpaid_tickets=Count("tickets", filter=Q(tickets__payment_status="pending")),
        )
    )
   
    total_events = events.count()
    upcoming_events = events.filter(start_time__gte=now())
    total_upcoming_events = events.filter(start_time__gte=now()).count()
    past_events = events.filter(start_time__lt=now())
    total_past_events = events.filter(start_time__lt=now()).count()
    # tickets = TicketType.objects.filter(organizer=event)
    
  
    context = {
         "total_events": total_events,
         "past_events":past_events,
         "upcoming_events": upcoming_events,
        "total_upcoming_events": total_upcoming_events,
        "total_past_events": total_past_events,
        "events": events,
            }

    return render(request, 'events/organizer_dashboard.html',context)

@login_required
def user_dashboard(request):
    tickets = Ticket.objects.filter(user=request.user)
     

    total_tickets = tickets.count()
    

    
    total_upcoming_events = Ticket.objects.upcoming_for_user(request.user).count()
    upcoming_events = Ticket.objects.upcoming_for_user(request.user)
    past_events = Ticket.objects.past_for_user(request.user)
    total_past_events = Ticket.objects.past_for_user(request.user).count()
    upcoming_tickets = tickets.filter(event__start_time__gte=now()).order_by('event__start_time')
    past_tickets = tickets.filter(event__start_time__lt=now()).order_by('event__start_time')

    context = {'upcoming_tickets':upcoming_tickets,
               'upcoming_events':upcoming_events,
               'past_events':past_events,
               'total_upcoming_events':total_upcoming_events,
               'total_past_events':total_past_events,
               'total_tickets':total_tickets,
               'tickets':tickets,
               'past_tickets':past_tickets,
               
               }
    

    return render(request,'events/user_dashboard.html', context)


@login_required
def profile(request):
    return render(request, "events/profile.html",{"user":request.user})


def redirect_after_login(request):
    user = request.user
    if user.is_authenticated:
        if user.is_organizer:
            return redirect('events:dashboard')
        return redirect('events:home')
    return redirect('accounts:login')

@login_required        
def purchase_ticket(request,event_id,ticket_type_id):
    event = get_object_or_404(Event, id=event_id)
    ticket_type = get_object_or_404(TicketType,id=ticket_type_id,event=event)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity',1))

        if not ticket_type.has_availability(quantity):
            print("Not enough tickets")
            messages.error(request, "Not enough tickets available")
            return redirect('events:user_dashboard') 
        
        ticket_type.quantity_available -= quantity
        ticket_type.save()

        ticket = Ticket.objects.create(
            event = event,
            user = request.user,
            ticket_type = ticket_type,
            quantity = quantity,
            payment_status= "pending",
            unique_code=str(uuid.uuid4())[:8]

        )
        messages.success(request,f" {ticket_type.name } Ticket reserved! Complete payment to confirm")
        print(f" {ticket_type.name } Ticket reserved! Complete payment to confirm")
        return redirect("events:user_dashboard")
    
    context = {'event':event,
               'ticket_type':ticket_type}
    return render(request,"events/purchase_ticket.html",context)