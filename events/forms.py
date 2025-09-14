from django import forms
from django.forms import inlineformset_factory
from .models import Event, TicketType

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title','description','event_image','venue','start_time','capacity']
        exclude = ['organizer','status']

        widgets = {
            'title':forms.TextInput(attrs={
                'class':'form-input w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition',
                'placeholder':'Enter event title'
            }),

            'description':forms.Textarea(attrs={
                'class':'form-textarea w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition',
                'placeholder':'Describe your event in details'
            }),

            'event_image':forms.ClearableFileInput(attrs={
                'class':'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder':'Click to upload your event image'
            }),

            'venue':forms.TextInput(attrs={
                'class':'form-input w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition',
                'placeholder':'Enter event Venue'
            }),
            'start_time': forms.DateTimeInput(attrs={
                "type":"datetime-local",
                "class":"form-input w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition",
        }),
            'end_time': forms.DateTimeInput(attrs={
                "type":"datetime-local",
                "class":"fform-input w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition",
        }),
            'capacity':forms.NumberInput(attrs={
                'class':'form-input w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition',
                'placeholder': 'Capacity'

            })
        }

class TicketTypeForm(forms.ModelForm):
    class Meta:
        model = TicketType
        fields = ['name','price','quantity_available']

        widgets = {
            'name':forms.TextInput(attrs={
                'class':'form-input w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition',
                'placeholder':'Ticket type(VIP,Regular,etc)'
            }),
            'price':forms.NumberInput(attrs={
                'class':'form-input w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition',
                'placeholder':'Ticket Price'
            }),
            
            'quantity_available':forms.NumberInput(attrs={
                'class':'form-input w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition',
                'placeholder':'Available quantity'
            }),
            
        }


TicketTypeFormSet = inlineformset_factory(Event
                                          ,TicketType,
                                          form=TicketTypeForm,
                                          extra=1,
                                          can_delete=True)