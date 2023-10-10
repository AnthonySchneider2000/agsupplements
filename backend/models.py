from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    units = models.CharField(max_length=100, blank=True) # blank=True allows the field to be blank
    
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.CharField(max_length=100, blank=True) # blank=True allows the field to be blank
    servings = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, through='ItemIngredient', related_name='items')
    tags = models.ManyToManyField('Tag', related_name='items')
    
    def __str__(self):
        return self.name
    

class ItemIngredient(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    mass = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return "ItemIngredient: " + self.item.name + ":" + self.ingredient.name
    
class BlacklistedItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)
    
    def __str__(self):
        return "BlacklistedItem: " + self.item.name + ":" + self.reason
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name