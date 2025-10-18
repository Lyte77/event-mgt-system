from allauth.account.forms import SignupForm,LoginForm
from django_countries.widgets import CountrySelectWidget
from django import forms 
from .models import UserProfile
class CustomSignupForm(SignupForm):
    is_organizer = forms.BooleanField(
        required=False,
        label="Signup as an organizer",
        help_text="Tick this box if you want to create and manage events"

    )
   


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for field in self.fields.values():
        #     field.widget.attrs.update({
        #         "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-600"
        #     })

        # self.fields["signup"].widget = forms.EmailInput({
        #     "class":"border-gray-300 focus:ring-2 focus:ring-orange-600",
        #     "placeholder": "Enter your email",
        # })

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
            'profile_pic': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:outline-none'
            }),
        }