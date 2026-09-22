from django.urls import path
from . import views

urlpatterns = [
    path('', views.IncidentListView.as_view(), name='incident-list'),
    path('incident/<int:pk>/', views.IncidentDetailView.as_view(), name='incident-detail'),
    path('incident/new/', views.IncidentCreateView.as_view(), name='incident-create'),
    path('incident/<int:pk>/edit/', views.IncidentUpdateView.as_view(), name='incident-update'),
]