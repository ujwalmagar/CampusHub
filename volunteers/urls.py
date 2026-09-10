from django.urls import path
from . import views

urlpatterns = [
    path('mine/', views.student_tasks, name='student_tasks'),
    path('mine/<int:pk>/update/', views.update_task_status, name='student_task_update'),
    path('manage/', views.VolunteerTaskManageView.as_view(), name='volunteer_manage'),
    path('create/', views.VolunteerTaskCreateView.as_view(), name='volunteer_create'),
    path('<int:pk>/update/', views.VolunteerTaskUpdateView.as_view(), name='volunteer_update'),
    path('<int:pk>/delete/', views.VolunteerTaskDeleteView.as_view(), name='volunteer_delete'),
]
