from django.urls import path
from . import views

app_name = "food"
urlpatterns = [
    path("", views.home, name="home"),
    path("ingredients/", views.ingredients, name="ingredients"),
    path("food/<str:name>", views.food_item, name="food_item"),
    path("food/", views.foods, name="foods"),
    path("add/", views.add, name="add"),
    path("delete/<str:name>/", views.delete, name="delete"),
    path("nutrition/<int:id>/", views.nutrition, name="nutrition"),
    path("nutrition/", views.nutrition, name="nutrition")
]
