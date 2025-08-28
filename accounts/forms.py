from allauth.account.forms import SignupForm
from django import forms 

class CustomSignupForm(SignupForm):
    is_organizer = forms.BooleanField(
        required=False,
        label="Signup as an organizer",
        help_text="Tick this box if you want to create and manage events"

    )

    def save(self,request):
        user = super().save(request)
        user.is_organizer = self.cleaned_data.get("is_organizer")
        user.save()
        return user