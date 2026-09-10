from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Event

def event_list(request):
    events = Event.objects.filter(status='OPEN')
    return render(request, 'events/list.html', {'events': events})

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class EventManageView(StaffRequiredMixin, ListView):
    model = Event
    template_name = 'events/manage.html'
    context_object_name = 'events'

class EventCreateView(StaffRequiredMixin, CreateView):
    model = Event
    template_name = 'events/form.html'
    fields = ['title', 'description', 'event_date', 'location', 'capacity', 'status']
    success_url = reverse_lazy('event_manage')

class EventUpdateView(StaffRequiredMixin, UpdateView):
    model = Event
    template_name = 'events/form.html'
    fields = ['title', 'description', 'event_date', 'location', 'capacity', 'status']
    success_url = reverse_lazy('event_manage')

class EventDeleteView(StaffRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/confirm_delete.html'
    success_url = reverse_lazy('event_manage')

    def delete(self, request, *args, **kwargs):
        """Soft delete by updating status to CANCELLED"""
        self.object = self.get_object()
        self.object.status = 'CANCELLED'
        self.object.save()
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(self.success_url)
