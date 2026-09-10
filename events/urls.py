from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('manage/', views.EventManageView.as_view(), name='event_manage'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
]
