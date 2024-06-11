from .serializers import AgentSerializer, PropertySerializer, PropertyListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Property, Agent
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
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        agent = self.get_object()
        if request.user.is_superuser or request.user == agent.user:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)


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
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        property = self.get_object()
        if request.user.is_superuser or request.user == property.user:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

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
