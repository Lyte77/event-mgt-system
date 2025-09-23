from allauth.account.forms import SignupForm,LoginForm
from django import forms 

class CustomSignupForm(SignupForm):
    is_organizer = forms.BooleanField(
        required=False,
        label="Signup as an organizer",
        help_text="Tick this box if you want to create and manage events"

    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-600"
            })

    def save(self,request):
        user = super().save(request)
        user.is_organizer = self.cleaned_data.get("is_organizer")
        user.save()
        return user
    

class CustomLoginForm(LoginForm):
    
 def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"].widget = forms.EmailInput(
            attrs={"class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-600"}
        )
        self.fields["password"].widget = forms.PasswordInput(
            attrs={"class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-600"}
        )
        self.fields["remember"].widget.attrs.update({"class": "h-4 w-4 text-orange-600 border-gray-300 rounded"})

   