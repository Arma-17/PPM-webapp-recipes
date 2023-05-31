from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden

from .models import Comment, Rating, Favorite
from . import models
from .models import Recipe

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
    template_name = 'recipes/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            recipe = self.object
            favorite = Favorite.objects.filter(user=self.request.user, recipe=recipe).first()
            context['favorite'] = favorite
        return context

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
        
    response_data = {
        'action': action
    }
    
    return JsonResponse(response_data)


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


@login_required
def add_comment(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    content = request.POST.get('content')
    comment = Comment(recipe=recipe, author=request.user, content=content)
    comment.save()
    return redirect('recipes-detail', pk=recipe_id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.author == request.user or comment.recipe.author == request.user:
        recipe_id = comment.recipe.id
        comment.delete()
        return redirect('recipes-detail', pk=recipe_id)
    else:
        return HttpResponseForbidden()

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    if user in comment.likes.all():
        comment.likes.remove(user)
    else:
        comment.likes.add(user)

    return redirect('recipes-detail', pk=comment.recipe.id)



class RecipeDetailView(DetailView):
    model = models.Recipe
    template_name = 'recipes/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            rating = Rating.objects.filter(recipe=self.object, user=self.request.user).first()
            context['user_rating'] = rating.rating if rating else None
        return context


@login_required
def rate_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    rating_value = int(request.POST.get('rating'))

    # Update existing rating or create a new one
    rating, created = Rating.objects.update_or_create(recipe=recipe, user=request.user, defaults={'rating': rating_value})

    if created:
        message = 'Rating added successfully.'
    else:
        message = 'Rating updated successfully.'

    return redirect(request.META.get('HTTP_REFERER'))