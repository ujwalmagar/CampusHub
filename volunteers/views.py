from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import VolunteerTask

# --- Admin Views ---
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class VolunteerTaskManageView(StaffRequiredMixin, ListView):
    model = VolunteerTask
    template_name = 'volunteers/manage.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        return VolunteerTask.objects.select_related('student', 'event').all()

class VolunteerTaskCreateView(StaffRequiredMixin, CreateView):
    model = VolunteerTask
    template_name = 'volunteers/form.html'
    fields = ['event', 'student', 'task_name', 'task_status']
    success_url = reverse_lazy('volunteer_manage')

class VolunteerTaskUpdateView(StaffRequiredMixin, UpdateView):
    model = VolunteerTask
    template_name = 'volunteers/form.html'
    fields = ['event', 'student', 'task_name', 'task_status']
    success_url = reverse_lazy('volunteer_manage')

class VolunteerTaskDeleteView(StaffRequiredMixin, DeleteView):
    model = VolunteerTask
    template_name = 'volunteers/confirm_delete.html'
    success_url = reverse_lazy('volunteer_manage')

# --- Student Views ---
@login_required
def student_tasks(request):
    try:
        student = request.user.student_profile
        tasks = VolunteerTask.objects.filter(student=student).select_related('event')
    except Exception:
        tasks = []
    return render(request, 'volunteers/my_tasks.html', {'tasks': tasks})

@login_required
def update_task_status(request, pk):
    if request.method == 'POST':
        new_status = request.POST.get('task_status')
        try:
            student = request.user.student_profile
            # IDOR Protection: Ensure task belongs to authenticated student
            task = get_object_or_404(VolunteerTask, pk=pk, student=student)
            if new_status in dict(VolunteerTask.STATUS_CHOICES):
                task.task_status = new_status
                task.save()
        except Exception:
            pass
    return redirect('student_tasks')
