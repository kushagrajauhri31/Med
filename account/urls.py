from django.urls import path,include
from account.views import Register,login,logout,cart,view_profile,remove_cart_item,profile_Update
from . import views

urlpatterns = [
    path("register",Register,name="reg"),
    path("login",login,name="login"),
    path("logout",logout,name="logout"),
    path("cart",cart,name="cart"),
    path("view_profile/",view_profile,name="view_profile"),
    path("profile_Update",profile_Update,name="profile_Update"),
    path('remove-cart-item', remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.payment_checkout, name='checkout_payment'),
    path('create_payment/', views.create_payment, name='create_payment'),
    path('execute_payment/', views.execute_payment, name='execute_payment'),
    #  path('download_report_file/<int:file_id>/', download_report_file, name='download_report_file'),
]
