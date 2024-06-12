from api.serializers import (
    AgentSerializer,
    FavoriteSerializer,
    ImageSerializer,
    PropertyListSerializer,
    PropertySerializer,
    ReviewSerializer,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models import Agent, Favorite, Property, PropertyImage, Review
from rest_framework import status
from django.db.models import Q
from users.permissions import CustomPermission
from rest_framework.permissions import IsAuthenticated


class AgentViewSet(ModelViewSet):
    queryset = Agent.objects.select_related("user").all()
    serializer_class = AgentSerializer
    permission_classes = [CustomPermission]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = []
        return super().get_permissions()


class PropertyViewSet(ModelViewSet):
    queryset = Property.objects.select_related("user").all()
    serializer_class = PropertySerializer
    permission_classes = [CustomPermission]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = []
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return PropertyListSerializer
        return PropertySerializer

    @action(detail=False, methods=["GET"])
    def search(self, request):
        query = request.query_params.get("name")
        location = request.query_params.get("location")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        filters = Q()
        if query:
            filters &= Q(name__icontains=query) | Q(description__icontains=query)
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

        properties = Property.objects.select_related("user").filter(filters)
        serializer = PropertyListSerializer(properties, many=True)
        return Response(serializer.data)


class ImageViewSet(ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [CustomPermission]

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


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.select_related("user", "property").all()
    serializer_class = ReviewSerializer
    permission_classes = [CustomPermission, IsAuthenticated]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = []
        return super().get_permissions()

    @action(detail=False, methods=["GET"])
    def get_reviews(self, request):
        property_id = request.query_params.get("property_id")

        if not property_id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"property_id": "This field is required in query params."},
            )

        reviews = Review.objects.select_related("user", "property").filter(
            property_id=property_id
        )
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.select_related("user", "property").all()
    serializer_class = FavoriteSerializer
    permission_classes = [CustomPermission, IsAuthenticated]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = []
        return super().get_permissions()

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def get_favorites(self, request):
        print(f"Authenticated user: {request.user}")
        favorites = Favorite.objects.select_related("user", "property").filter(
            user=request.user
        )
        print(f"Favorites fetched: {favorites}")

        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
