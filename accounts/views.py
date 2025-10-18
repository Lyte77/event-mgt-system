from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm

# Create your views here.
@login_required
def edit_user_profile(request):
    profile = request.user.profile
    form = UserProfileForm(instance=profile)
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
           profile = form.save(commit=False)
           profile.is_completed = True
           profile.save()
           return redirect('events:dashboard_router')
        
       

    
    # if request.path == reverse('accounts:profile_onboarding'):
    #     onboarding = True
    #     print("Onboarding")
    # else:
    #     onboarding = False
    #     print("no onboarding")

    

    # form = UserProfileForm()
    context = {'form':form,
               }
    return render(request, 'accounts/profile_page.html',context)

            

