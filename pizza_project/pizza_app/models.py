from django.db import models

class Size(models.Model):
    pizza_size = models.CharField(max_length=100)

    def __str__(self):
        return self.pizza_size

class Pizza(models.Model):
    topping1 = models.CharField(max_length=100)
    topping2 = models.CharField(max_length=100)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    def __str__(self):
        return '{} Pizza {} , {}'.format(self.size.pizza_size,self.topping1,self.topping2)
