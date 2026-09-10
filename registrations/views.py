from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Registration

@login_required
def my_registrations(request):
    try:
        registrations = Registration.objects.filter(student=request.user.student_profile).select_related('event')
    except Exception:
        registrations = []
    return render(request, 'registrations/my_registrations.html', {'registrations': registrations})
