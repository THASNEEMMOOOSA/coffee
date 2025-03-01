from django.db import models


# Create your models here.
class Coffee(models.Model):
    name=models.TextField(max_length=20)
    quantity=models.TextField(max_length=10)
    price=models.IntegerField(null=True)
    image=models.ImageField(upload_to='coffee_images/', blank=True, null=True)

class Cart(models.Model):
    itemname=models.TextField(max_length=20)
    itemquantity=models.TextField(max_length=10)
    itemprice=models.IntegerField(null=True)
    itemqnt=models.IntegerField(null=True)
    userid=models.TextField(max_length=20)
    total=models.IntegerField(null=True)
    # image=models.ImageField(upload_to='coffee_images/', blank=True, null=True)
    imag=models.TextField(max_length=100)

class Orderp(models.Model):
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    phone=models.CharField(max_length=20)
    address=models.CharField(max_length=20)
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20) 
    zipcode=models.CharField(max_length=20)
    userid=models.TextField(max_length=20)
    amount=models.IntegerField(null=True)
    ispaid=models.BooleanField(default=False)
    razorpay_order_id=models.CharField(max_length=20,null=True)
    razorpay_payment_id=models.CharField(max_length=20,null=True)
    razorpay_payment_signature=models.CharField(max_length=20,null=True)








class  Checkout(models.Model):
    subtotal=models.IntegerField(null=True)
    tax=models.IntegerField(null=True)     
    totalprice=models.IntegerField(null=True)    
    userids=models.TextField(max_length=20)


class Invoice(models.Model):
    iuserids=models.TextField(max_length=20)
    # ifname=models.CharField(max_length=20)
    # ilname=models.CharField(max_length=20)
    iamount=models.IntegerField(null=True)
    irazorpay_order_id=models.CharField(max_length=20,null=True)


