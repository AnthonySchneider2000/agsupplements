from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class ItemWithIngredients(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ingredients = models.ManyToManyField(Ingredient, through='ItemIngredient', related_name='items')

class ItemIngredient(models.Model):
    item = models.ForeignKey(ItemWithIngredients, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    mass = models.DecimalField(max_digits=10, decimal_places=2)