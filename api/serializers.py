from rest_framework import serializers
from api.models import Property, Agent, PropertyImage
from users.serializers import UserSerializer


class AgentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=Agent.objects.all(), source="user", write_only=True
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


class PropertySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(), source="user", write_only=True
    )
    images = ImageSerializer(many=True, read_only=True)

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
        ]
