from allauth.account.forms import SignupForm,LoginForm
from django_countries.widgets import CountrySelectWidget
from django import forms 
from .models import UserProfile



class CustomSignupForm(SignupForm):
    is_organizer = forms.BooleanField(
        required=False,
        label="Signup as an organizer",
        help_text="Tick this box if you want to create and manage events",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define base styles per input type
        text_input_class = "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-600"
        checkbox_class = "h-4 w-4 text-orange-600 focus:ring-orange-500 border-gray-300 rounded"

        for name, field in self.fields.items():
            widget = field.widget

            # Apply per-widget customization
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({"class": checkbox_class})
            elif isinstance(widget, (forms.PasswordInput, forms.EmailInput, forms.TextInput)):
                widget.attrs.update({"class": text_input_class})
            else:
                # fallback for other field types (optional)
                widget.attrs.update({"class": text_input_class})


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

class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = "widgets/custom_clearable_file_input.html"

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user','is_completed']

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-600 focus:border-transparent',
                'placeholder': 'Enter your full name'
            }),
            'country': CountrySelectWidget(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-600 focus:border-transparent'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-600 focus:border-transparent',
                'placeholder': 'Enter phone number'
            }),
            'about_organizer': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-600 focus:border-transparent resize-none',
                'placeholder': 'Tell us about yourself/organization',
                'rows': 4
            }),
            'profile_pic': CustomClearableFileInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:outline-none'
            }),
        }