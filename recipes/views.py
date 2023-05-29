from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from . import models

# Create your views here.
def index(request):
    recipes = models.Recipe.objects.all()

    context={
        'recipes':recipes
    }
    return render(request,"recipes/index.html",{'title':'Home'},context)

class RecipeListView(ListView):
    model=models.Recipe
    template_name='recipes/index.html'
    context_object_name = 'recipes'

class RecipeDetailView(DetailView):
    model=models.Recipe

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = models.Recipe
    fields = ['img', 'title', 'description'] 

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = models.Recipe
    fields = ['img', 'title', 'description']

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = models.Recipe
    success_url = reverse_lazy('recipes-home')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author


def about(request):
    return render(request,"recipes/about.html",{'title':'about us page'})


@login_required
def toggle_favorite(request, recipe_id):
    recipe = models.Recipe.objects.get(id=recipe_id)
    favorite, created = models.Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    if created:
        action = 'add'
    else:
        favorite.delete()
        action = 'remove'
    response = {
        'action': action
    }
    return JsonResponse(response)


def search_results(request):
    query = request.GET.get('query')

    recipes = models.Recipe.objects.filter(
        Q(title__icontains=query) | Q(author__username__icontains=query) | Q(description__icontains=query)
    )
    context = {
        'query': query,
        'recipes': recipes,
    }
    return render(request, 'recipes/search_results.html', context)