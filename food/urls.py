from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("ingredients/", views.ingredients, name="ingredients"),
    path("food/", views.food, name="food"),
    path("suggestions/", views.suggestions, name="suggestions"),
    path("recipe/", views.recipe, name="recipe")
]
