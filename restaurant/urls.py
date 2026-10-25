from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/', views.book, name='book'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu, name='menu'),
    path('bookings/', views.bookings, name='bookings'),
    path('reservations/', views.reservations, name='reservations'),
    path('menu-items/', views.MenuItemsView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>/', views.SingleMenuItemView.as_view(), name='single-menu-item'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
]
