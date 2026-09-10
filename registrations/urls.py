from django.urls import path
from . import views

urlpatterns = [
    path('mine/', views.my_registrations, name='my_registrations'),
]
