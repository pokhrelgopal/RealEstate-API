from rest_framework import serializers
from .models import Property, Agent
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
        ]
