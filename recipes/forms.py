from django import forms
from .models import Recipe, Comment, Rating

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'img', 'category', 'ingredients']  # Aggiungi gli altri campi necessari

    # Metodo per "processare" gli ingredienti
    def clean_ingredients(self):
        ingredients = self.cleaned_data.get('ingredients')
        if ingredients:
            # Puoi fare qui una pulizia aggiuntiva se necessario
            return ingredients
        return ''

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
