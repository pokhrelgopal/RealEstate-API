from django.contrib import admin
from api.models import Agent, Property, PropertyImage

admin.site.register(Property)
admin.site.register(PropertyImage)
admin.site.register(Agent)
