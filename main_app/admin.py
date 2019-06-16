from django.contrib import admin

# Register your models here.
from .models import Car, Service, Accessory, Photo

admin.site.register(Car)
admin.site.register(Service)
admin.site.register(Accessory)
admin.site.register(Photo)
