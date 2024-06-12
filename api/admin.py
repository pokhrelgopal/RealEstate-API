from django.contrib import admin
from api.models import Agent, Property, PropertyImage, Review, Favorite

admin.site.register(Property)
admin.site.register(PropertyImage)
admin.site.register(Agent)
admin.site.register(Review)
admin.site.register(Favorite)
