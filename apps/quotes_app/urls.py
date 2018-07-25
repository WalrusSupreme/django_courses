from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('quotes', views.quotes),
    path('logout', views.logout),
    path('addquote', views.addquote),
    path('users/<int:user_id>', views.users),
    path('favorite/<int:quote_id>', views.favorite),
    path('remove/<int:quote_id>', views.remove)
]