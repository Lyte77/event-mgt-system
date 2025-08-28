from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        exclude = ['organizer','status']

        widgets = {
            'start_time': forms.DateTimeInput(attrs={
                "type":"datetime-local",
                "class":"form-input",
        }),
            'end_time': forms.DateTimeInput(attrs={
                "type":"datetime-local",
                "class":"form-input",
        })
        }