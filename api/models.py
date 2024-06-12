from django.db import models
from users.models import User


class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ("house", "House"),
        ("apartment", "Apartment"),
        ("land", "Land"),
        ("commercial", "Commercial"),
    ]

    PROPERTY_STATUS_CHOICES = [
        ("available", "Available"),
        ("sold", "Sold"),
        ("rented", "Rented"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties")
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField(
        upload_to="properties/",
        null=True,
        blank=True,
        default="property_thumbnail/default.png",
    )
    property_type = models.CharField(
        max_length=10,
        choices=PROPERTY_TYPE_CHOICES,
        default="house",
    )
    status = models.CharField(
        max_length=10,
        choices=PROPERTY_STATUS_CHOICES,
        default="available",
    )
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    size = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def can_change(self, user):
        return self.user == user

    class Meta:
        db_table = "property"
        verbose_name_plural = "Properties"


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="property_images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.property.title

    def can_change(self, user):
        return self.property.user == user

    class Meta:
        db_table = "property_image"
        verbose_name_plural = "Property Images"


class Agent(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="agent_profile"
    )
    agency_name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=100)
    experience_years = models.IntegerField()
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    def can_change(self, user):
        return self.user.is_superuser or self.user == user

    class Meta:
        db_table = "agent"
        verbose_name_plural = "Agents"
