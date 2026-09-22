from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.core.mail import send_mail
from django.conf import settings
from .models import Incident
from .forms import IncidentForm


class IncidentListView(LoginRequiredMixin, ListView):
    """Shows all incidents. Any logged-in user can view this."""
    model = Incident
    template_name = 'incidents/incident_list.html'
    context_object_name = 'incidents'
    paginate_by = 10

    def get_queryset(self):
        queryset = Incident.objects.all().order_by('-created_at')
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class IncidentDetailView(LoginRequiredMixin, DetailView):
    """Shows one incident's full details."""
    model = Incident
    template_name = 'incidents/incident_detail.html'
    context_object_name = 'incident'


class IncidentCreateView(LoginRequiredMixin, CreateView):
    """Any logged-in user can log a new incident. Sends an email on creation."""
    model = Incident
    form_class = IncidentForm
    template_name = 'incidents/incident_form.html'
    success_url = reverse_lazy('incident-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        send_mail(
            subject=f"New Incident Logged: {self.object.title}",
            message=(
                f"A new incident has been created.\n\n"
                f"Title: {self.object.title}\n"
                f"Priority: {self.object.get_priority_display()}\n"
                f"Description: {self.object.description}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.INCIDENT_NOTIFY_EMAIL],
            fail_silently=True,
        )
        return response


class IncidentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Only staff/admin users can edit or resolve an incident.
    Sends an email specifically when status changes to 'resolved'."""
    model = Incident
    form_class = IncidentForm
    template_name = 'incidents/incident_form.html'
    success_url = reverse_lazy('incident-list')

    def test_func(self):
        # Role-based access: only staff accounts can reach this view.
        return self.request.user.is_staff

    def form_valid(self, form):
        old_status = Incident.objects.get(pk=self.object.pk).status
        response = super().form_valid(form)
        if old_status != 'resolved' and self.object.status == 'resolved':
            send_mail(
                subject=f"Incident Resolved: {self.object.title}",
                message=f"The incident '{self.object.title}' has been marked resolved.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.INCIDENT_NOTIFY_EMAIL],
                fail_silently=True,
            )
        return response
