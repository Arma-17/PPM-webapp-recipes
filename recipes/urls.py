from django.urls import path
from . import views

'app/model_viewtype'
'recipes/recipe_detail.html'

urlpatterns = [
    path("", views.RecipeListView.as_view(), name="recipes-home"),
    path("recipe/<int:pk>/", views.RecipeDetailView.as_view(), name="recipes-detail"),
    path("recipe/create/", views.RecipeCreateView.as_view(), name="recipes-create"),
    path("recipe/<int:pk>/update/", views.RecipeUpdateView.as_view(), name="recipes-update"),
    path("recipe/<int:pk>/delete/", views.RecipeDeleteView.as_view(), name="recipes-delete"),
    path("about/", views.about, name="recipes-about"),
    path('recipes/<int:recipe_id>/toggle_favorite/', views.toggle_favorite, name='toggle-favorite'),
    path("search/", views.search_results, name="recipes-search"),
    path("recipe/<int:recipe_id>/add-comment/", views.add_comment, name="add-comment"),
]
