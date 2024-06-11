from .serializers import (
    AgentSerializer,
    PropertySerializer,
    PropertyListSerializer,
    ImageSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Property, Agent, PropertyImage
from rest_framework import status
from django.db.models import Q


class AgentViewSet(ModelViewSet):
    queryset = Agent.objects.select_related("user").all()
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = []
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        agent = self.get_object()
        if request.user.is_superuser or request.user == agent.user:
            return super().update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Forbidden."})

    def destroy(self, request, *args, **kwargs):
        agent = self.get_object()
        if request.user.is_superuser or request.user == agent.user:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Forbidden."})


class PropertyViewSet(ModelViewSet):
    queryset = Property.objects.select_related("user").all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = []
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return PropertyListSerializer
        return PropertySerializer

    def update(self, request, *args, **kwargs):
        property = self.get_object()
        if request.user.is_superuser or request.user == property.user:
            return super().update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Forbidden."})

    def destroy(self, request, *args, **kwargs):
        property = self.get_object()
        if request.user.is_superuser or request.user == property.user:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Forbidden."})

    @action(detail=False, methods=["GET"])
    def search(self, request):
        query = request.query_params.get("name", "")
        location = request.query_params.get("location", "")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        filters = Q()
        if query:
            filters &= Q(name__icontains=query) or Q(description__icontains=query)
        if location:
            filters &= (
                Q(address__icontains=location)
                | Q(city__icontains=location)
                | Q(state__icontains=location)
            )
        if min_price:
            filters &= Q(price__gte=min_price)
        if max_price:
            filters &= Q(price__lte=max_price)

        properties = Property.objects.filter(filters)
        serializer = PropertyListSerializer(properties, many=True)
        return Response(serializer.data)


class ImageViewSet(ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = ImageSerializer

    # ! LIST RETRIEVE and UPDATE are forbidden because images will only be shown in the property detail view.
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Forbidden."})

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Forbidden."})

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Forbidden."})

    def destroy(self, request, *args, **kwargs):
        image = self.get_object()
        if request.user.is_superuser or request.user == image.property.user:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Forbidden."})

    # ? User can add image to property only if they are the owner of the property.
    def create(self, request, *args, **kwargs):
        property_id = request.data.get("property_id")
        if not property_id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"property_id": "This field is required."},
            )
        property = Property.objects.get(pk=request.data.get("property_id"))
        if request.user == property.user:
            return super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Forbidden."})

    def get_permissions(self):
        if self.action == "create" or self.action == "destroy":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
