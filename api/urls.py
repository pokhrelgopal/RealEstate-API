from django.urls import path
from rest_framework.routers import DefaultRouter
from api.views import *

router = DefaultRouter()

router.register(r"agents", AgentViewSet, basename="agents")
router.register(r"properties", PropertyViewSet, basename="properties")
router.register(r"images", ImageViewSet, basename="images")
router.register(r"reviews", ReviewViewSet, basename="reviews")
router.register(r"favorites", FavoriteViewSet, basename="favorites")

urlpatterns = []

urlpatterns += router.urls
