from django.contrib import admin
from .models import Agent, Property, PropertyImage

admin.site.register(Property)
admin.site.register(PropertyImage)
admin.site.register(Agent)
