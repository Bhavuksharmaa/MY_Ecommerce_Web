from django.db import models
from datetime import date

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=50,default="")
    Desc =models.CharField(max_length=1500,default="")
    category = models.CharField(max_length=50,default="")
    subcategory = models.CharField(max_length=50,default="")
    price = models.IntegerField(default=0)
    image=models.ImageField(upload_to="shop/images",default="")
    pub_date =models.DateField()

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length=70, default="")
    phone = models.IntegerField( default="0")
    desc = models.CharField(max_length=1500, default="")

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    item_json = models.CharField(max_length=4000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    phone = models.IntegerField(default="0")
    zip_code = models.IntegerField( default="0")

    def __str__(self):
        return self.name

class OrderUpdate(models.Model):
    udate_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
