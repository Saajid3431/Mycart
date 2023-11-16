from django.urls import path
from.import   views




urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signupp, name="signup"),
    path('login', views.loginn, name="login"),
    path('logout', views.logout, name="logout"),
    path('category', views.category, name="category"),
    path('add-to-cart', views.addtocart, name="addtocart"),
    path('cartview', views.cartview, name="cartview"),
    path('update-cart', views.updatecart, name="updatecart"),
    path('faq', views.faq, name="faq"),
    path('home/<str:cate_slug>/<str:prod_slug>', views.productview, name="productview"),
    path('home/<str:slug>', views.products, name="products"),
    path('home', views.home, name="home"),
    path('delete-cart-item' , views.deletecartitem,name="deletecartitem "),
    path('placeorder', views.placeorder, name="placeorder"),
    path('product-list', views.productlistajax),
    path('searchproduct' , views.searchproduct, name="searchproduct"),
]

