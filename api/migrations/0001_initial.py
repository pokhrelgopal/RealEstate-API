# Generated by Django 5.0.6 on 2024-06-11 07:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Agent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("agency_name", models.CharField(max_length=100)),
                ("license_number", models.CharField(max_length=100)),
                ("experience_years", models.IntegerField()),
                ("bio", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="agent_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Agents",
                "db_table": "agent",
            },
        ),
        migrations.CreateModel(
            name="Property",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "property_type",
                    models.CharField(
                        choices=[
                            ("house", "House"),
                            ("apartment", "Apartment"),
                            ("land", "Land"),
                            ("commercial", "Commercial"),
                        ],
                        default="house",
                        max_length=10,
                    ),
                ),
                ("address", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("zipcode", models.CharField(max_length=10)),
                ("bedrooms", models.IntegerField(blank=True, null=True)),
                ("bathrooms", models.IntegerField(blank=True, null=True)),
                ("size", models.DecimalField(decimal_places=2, max_digits=10)),
                ("is_available", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="properties",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Properties",
                "db_table": "property",
            },
        ),
    ]
