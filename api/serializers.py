import django.db
from rest_framework import serializers
from api.models import Agent, Favorite, Property, PropertyImage, Review
from users.serializers import UserListSerializer, UserSerializer
from users.models import User


class AgentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )

    class Meta:
        model = Agent
        fields = [
            "id",
            "user",
            "user_id",
            "agency_name",
            "license_number",
            "experience_years",
            "bio",
        ]


class ImageSerializer(serializers.ModelSerializer):
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(), source="property", write_only=True
    )

    class Meta:
        model = PropertyImage
        fields = ["id", "image", "property_id"]


class PropertyListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "user",
            "title",
            "price",
            "property_type",
            "thumbnail",
            "address",
            "city",
            "state",
            "bedrooms",
            "bathrooms",
            "size",
            "status",
            "updated_at",
        ]


class ReviewListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )

    class Meta:
        model = Review
        fields = ["id", "user", "user_id", "rating", "review", "created_at"]


class PropertySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )
    images = ImageSerializer(many=True, read_only=True)
    reviews = ReviewListSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "user",
            "user_id",
            "title",
            "description",
            "price",
            "property_type",
            "address",
            "city",
            "state",
            "zipcode",
            "bedrooms",
            "bathrooms",
            "size",
            "status",
            "created_at",
            "updated_at",
            "images",
            "reviews",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(), source="property", write_only=True
    )
    property = PropertyListSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "user_id",
            "property",
            "property_id",
            "rating",
            "review",
            "created_at",
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    property = PropertyListSerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(), source="property", write_only=True
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "user", "user_id", "property", "property_id"]
