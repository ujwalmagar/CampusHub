from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    StudentViewSet,
    EventViewSet,
    RegistrationViewSet,
    VolunteerTaskViewSet
)
from .auth_views import api_signup, api_login
from .report_views import event_participation_report, student_participation_report

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'events', EventViewSet)
router.register(r'registrations', RegistrationViewSet)
router.register(r'volunteer-tasks', VolunteerTaskViewSet)

urlpatterns = [
    # Auth endpoints
    path('auth/signup/', api_signup, name='api_signup'),
    path('auth/login/', api_login, name='api_login'),
    
    # Reports endpoints
    path('reports/events/<int:pk>/participation/', event_participation_report, name='event_report'),
    path('reports/students/<int:pk>/participation/', student_participation_report, name='student_report'),
    
    # Automatically generated standard CRUD and @action endpoints
    path('', include(router.urls)),
]
