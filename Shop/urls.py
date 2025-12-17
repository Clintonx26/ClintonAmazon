from django.urls import path 
from . import views


app_name = 'shop'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('/cart/<int:product_id>/', views.add_to_cart, name='cart'),
    path('orders/', views.orders, name='orders'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('delete/<int:id>/', views.delete_item, name="delete"),
    path('decrease/<int:id>/', views.decrease_item, name="decrease"),
    path('increase/<int:id>/', views.increase_item, name="increase"),
    path('checkout/', views.checkout, name="checkout"),
    path('orders/', views.order_list, name="orders"),
    path('detail/<int:order_id>/', views.order_details, name="detail")
]
