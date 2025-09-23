from django import forms
from django.forms import inlineformset_factory
from .models import Event, TicketType
from django.utils.timezone import now

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title','description','event_image','venue','start_time', 'end_time', 'capacity']
        exclude = ['organizer','status']

        widgets = {
            'title':forms.TextInput(attrs={
                'class':'w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2  focus:outline-none',
                'placeholder':'Enter event title'
            }),

            'description':forms.Textarea(attrs={
                'class':'w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2  focus:outline-none',
                'placeholder':'Describe your event in details'
            }),

            "event_image": forms.ClearableFileInput(attrs={
                "class": "w-full px-4 py-2 rounded-lg border border-gray-300 bg-white cursor-pointer focus:ring-2  focus:outline-none",
            }),

            'venue':forms.TextInput(attrs={
                'class':'w-full px-4 py-2 rounded-lg border border-gray-300  focus:outline-none',
                'placeholder':'Enter event Venue'
            }),
              "start_time": forms.DateTimeInput(attrs={
                "class": "w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2  focus:outline-none",
                "type": "datetime-local"
            }),
            "end_time": forms.DateTimeInput(attrs={
                "class": "w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2  focus:outline-none",
                "type": "datetime-local"
        }),
            'capacity':forms.NumberInput(attrs={
                'class':'form-input w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition',
                'placeholder': 'Capacity'

            })
        }



    def clean(self):
        """ Custom validation for event times """
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and start_time < now():
            self.add_error("start_time", "Start time cannot be in the past.")

        if start_time and end_time and end_time <= start_time:
            self.add_error("end_time", "End time must be after the start time.")

        return cleaned_data


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
                                          extra=4,
                                          can_delete=True)