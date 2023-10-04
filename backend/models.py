from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.CharField(max_length=100, blank=True) # blank=True allows the field to be blank
    servings = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, through='ItemIngredient', related_name='items')
    

class ItemIngredient(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    mass = models.DecimalField(max_digits=10, decimal_places=2)
    
class BlacklistedItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)