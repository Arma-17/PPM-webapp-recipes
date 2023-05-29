from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from recipes.models import Recipe
from . import models 
from . import forms

# Create your views here.
def register(request):
    if request.method=="POST":
        form=forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f"{username}, you're account has been created!, please login ")
            return redirect('user-login')
    else:    
        form = forms.UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required()
def profile(request):
    return render(request, 'users/profile.html',{'title':'My Profile'})

def favorites(request):
    return render(request, 'users/favorites.html',{'title':'Favorites'})

def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user)
    context = {
        'recipes': recipes
    }
    
    return render(request, 'users/my-recipes.html', context)         #TODO change name 

