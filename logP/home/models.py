from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category (models.Model):
    slug=models.CharField(max_length=50,null=False,blank=False)
    category_name=models.CharField(max_length=50,null=False,blank=False)
    category_disc=models.CharField(max_length=80,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0=default,1=hidden")
    trending=models.BooleanField(default=False,help_text="0=default,1=hidden")
    def __str__(self):
        return self.category_name
    
class Products (models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    slug=models.CharField(max_length=100,null=False,blank=False)
    product_name=models.CharField(max_length=100,null=False,blank=False)
    produt_image_1=models.ImageField(upload_to="imagess",null=False,blank=False)
    discription=models.CharField(max_length=500,null=False,blank=False)
    quantity=models.IntegerField(null=False,blank=False)
    original_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0=default,1=hidden")
    trending=models.BooleanField(default=False,help_text="0=default,1=hidden")
    def __str__(self):
        return self.product_name


# Carousal
class Carousal (models.Model):
    carousal_img_1=models.ImageField(upload_to="imagess",null=False,blank=False)
    carousal_img_2=models.ImageField(upload_to="imagess",null=False,blank=False)
    carousal_img_3=models.ImageField(upload_to="imagess",null=False,blank=False)


class Cart (models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Products, on_delete=models.CASCADE)
    product_qty= models.IntegerField(null=False, blank=False)
    created_at= models.DateTimeField(auto_now_add=True)



    

    

    

