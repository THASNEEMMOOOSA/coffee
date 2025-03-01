"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ansh import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home),
    path('form/', views.addform),
    path('store/', views.store),
    # path('cart/showcart/', views.showcart),
    
    # path('form/add/', views.add),
    path('form/add/', views.add,),
    path('form/addaddsuccess/', views.addsuccess),
    path('items/<int:id>/updateform/', views.updateform),
    path('updatesuccess/', views.updatesuccess),
    path('items/<int:id>/updateform/updatesuccess/', views.update),
    path('items/', views.items),
    path('removed/', views.removed),
    path('items/<int:id>/remove/', views.remove),

    # path('store/<int:id>/cart/', views.cart),
    # path('cart/', views.mycart),
    path('showcart/', views.showcart),
    path('showcart/remove/<str:itemname>/<str:userid>/', views.remove_cart_item),


    path('store/<int:id>/buyform/', views.buyform),
    path('store/<int:id>/buyform1/', views.buyform1),


    
    # path('store/<int:id>/addtocart/', views.addtocart),

    path("showcart/<str:itemname>/removecart/<str:userid>/", views.cartremove),


    # path('purchased/<str:paymentid>/<str:orderid>/<str:paymentsignature>/',views.purchased),
    path('purchased/<str:paymentid>/<str:orderid>/',views.purchased),

    path('payfail/',views.payfail),

    path('store/<int:id>/buyform1/purchased/',views.buy),
    path('store/<int:id>/buyform/purchased/',views.addtocart),
    path("registerform/",views.registerform),
    path("registerform/submit/",views.register),
    path("",views.loginform),
    path("login/",views.loginpage),
    path("logout/",views.log_out),
    path('showcart/checkout/', views.checkout),
    path('showcart/checkout/purchased/', views.ordernow),
    path('myorder/', views.yourorder),
    path('cancel/', views.ordercancel),
    # path('clear/', views.clearcart),
    path('testr/<str:userid>/', views.testr),



    












    # path('', views.updateform),


    






]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
        
