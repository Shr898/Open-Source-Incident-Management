from rest_framework import viewsets, permissions
from .models import Incident
from .serializers import IncidentSerializer


class IncidentViewSet(viewsets.ModelViewSet):
    """
    Exposes full CRUD as a REST API:
    GET    /api/incidents/         -> list
    POST   /api/incidents/         -> create
    GET    /api/incidents/<id>/    -> retrieve
    PUT    /api/incidents/<id>/    -> full update
    PATCH  /api/incidents/<id>/    -> partial update (e.g. just status)
    DELETE /api/incidents/<id>/    -> delete
    """
    queryset = Incident.objects.all().order_by('-created_at')
    serializer_class = IncidentSerializer
    permission_classes = [permissions.IsAuthenticated]
