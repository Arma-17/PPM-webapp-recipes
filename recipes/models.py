from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

CATEGORY_CHOICES = [
    ('first', 'First'),
    ('second', 'Second'),
    ('side', 'Side'),
    ('dessert', 'Dessert'),
]

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    img = models.ImageField(upload_to="recipes/", blank=False, null=False)
    ingredients = models.TextField(blank=False, default='')    
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES,  default='first')


    def get_absolute_url(self):
        return reverse('recipes-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
    
    def average_rating(self):
        ratings = Rating.objects.filter(recipe=self)
        if ratings.exists():
            total_ratings = ratings.count()
            sum_ratings = ratings.aggregate(models.Sum('rating'))['rating__sum']
            average = sum_ratings / total_ratings
            return round(average, 1)
        else:
            return None



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.recipe.title}"    

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments')

    def __str__(self):
        return f"Comment by {self.author.username} on {self.recipe.title}"    
    
class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    class Meta:
        unique_together = ('recipe', 'user')

    def __str__(self):
        return f"Rating {self.rating} by {self.user.username} on {self.recipe.title}"    