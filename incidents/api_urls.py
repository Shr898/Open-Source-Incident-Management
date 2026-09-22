from rest_framework.routers import DefaultRouter
from .api import IncidentViewSet

router = DefaultRouter()
router.register(r'incidents', IncidentViewSet, basename='incident-api')

urlpatterns = router.urls
