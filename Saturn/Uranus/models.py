from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    CATEGORY_PRODUCT=(
        ('Sofa', 'Sofa'),
        ('Chair', 'Chair')
    )
    name= models.CharField(max_length=100, null=True)
    product_image= models.ImageField(upload_to='img')
    price= models.IntegerField()
    category= models.CharField(choices=CATEGORY_PRODUCT, max_length=6, null=True)
    description= models.TextField(null=True)
    date_created= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    quantity = models.PositiveIntegerField(default=1)