from django.contrib import admin
from .models import Ingredient, UserIngredient
# Register your models here.

admin.site.register(Ingredient)
admin.site.register(UserIngredient)