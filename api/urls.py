from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r"agents", AgentViewSet, basename="agents")
router.register(r"properties", PropertyViewSet, basename="properties")

urlpatterns = []

urlpatterns += router.urls
