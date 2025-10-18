from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        if request.user.is_authenticated:
           profile = getattr(request.user,'profile',None)
           onboarding_url = reverse('accounts:profile_onboarding')

           if profile and not profile.is_completed:
               if request.path not in [onboarding_url,reverse('account_logout')]:
                   return redirect("accounts:profile_onboarding")
        return self.get_response(request)


