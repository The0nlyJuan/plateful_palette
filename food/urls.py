from django.urls import path
from . import views

app_name = "food"
urlpatterns = [
    path("", views.home, name="home"),
    path("ingredients/", views.ingredients, name="ingredients"),
    path("food/<int:id>", views.food, name="food"),
    path("add/", views.add, name="add"),
    path("delete/<int:id>/", views.delete, name="delete"),
    path("nutrition/<int:id>/", views.nutrition, name="nutrition")
]
