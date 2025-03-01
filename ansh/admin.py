from django.contrib import admin
from .models import Coffee,Cart,Orderp,Checkout,Invoice
# Register your models here.

class Coffeadmin(admin.ModelAdmin):
    list_display=["name","price"]
admin.site.register(Coffee,Coffeadmin)

class Cartadmin(admin.ModelAdmin):
    list_display=['userid',"itemname",'itemprice']
admin.site.register(Cart,Cartadmin)

class Orderadmin(admin.ModelAdmin):
    list_display=['fname',"lname",'userid','ispaid']
admin.site.register(Orderp,Orderadmin)

class Checkoutadmin(admin.ModelAdmin):
    list_display=['userids','subtotal','tax','totalprice' ]
admin.site.register(Checkout,Checkoutadmin)

class Invoiceadmin(admin.ModelAdmin):
    list_display=['iuserids','iamount','irazorpay_order_id' ]
admin.site.register(Invoice,Invoiceadmin)




