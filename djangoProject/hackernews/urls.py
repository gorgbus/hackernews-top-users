from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_users),
    path('api/users', views.get_data)
]