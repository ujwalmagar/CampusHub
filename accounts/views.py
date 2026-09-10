from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return '/accounts/dashboard/'

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in automatically after successful signup.
            # We must explicitly specify the backend since we have multiple backends configured.
            from django.contrib.auth import login
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
        
    return render(request, 'accounts/signup.html', {'form': form})

from students.models import Student
from events.models import Event
from registrations.models import Registration
from volunteers.models import VolunteerTask

@login_required
def dashboard_redirect(request):
    """
    Renders the appropriate dashboard based on user role.
    """
    if request.user.is_staff:
        context = {
            'total_students': Student.objects.count(),
            'total_events': Event.objects.count(),
            'total_registrations': Registration.objects.count(),
            'pending_registrations': Registration.objects.filter(status='PENDING').select_related('student', 'event').order_by('-registered_at')[:10],
            'total_volunteers': VolunteerTask.objects.count()
        }
        return render(request, 'dashboard/admin.html', context)
    else:
        try:
            student = request.user.student_profile
            context = {
                'my_registrations': Registration.objects.filter(student=student).select_related('event')[:5],
                'my_volunteer_tasks': VolunteerTask.objects.filter(student=student).select_related('event'),
                'upcoming_events': Event.objects.filter(status='OPEN')[:5]
            }
        except Exception:
            context = {}
            
        return render(request, 'dashboard/student.html', context)
