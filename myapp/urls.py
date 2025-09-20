from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',register,name='register'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('home/',ProductsViews.as_view(),name='home'),
    path('create_product/',CreateProducts.as_view(),name='create_product'),
    path('update_product/<int:pk>/',UpdateProducts.as_view(),name='update_product'),
    path('delete_product/<int:pk>/',DeleteProducts.as_view(),name='delete_product'),
    path('detail_product/<int:pk>/',DetailProducts.as_view(),name='detail_product'),
    path('cart/',CartView.as_view(),name='cart'),
    path('add_to_cart/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove_from_cart/<int:pk>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('create_order/', CreateOrderView.as_view(), name='create_order'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('delete_order/<int:pk>/', OrderDelete.as_view(), name='delete_order'),
    path('order_detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('profile/', profile, name='profile'),
    path('update_profile/', update_profile, name='update_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)