"""admin.py import statements"""
from django.contrib import admin
from .models import CarMake, CarModel


class CarModelInline(admin.StackedInline):
    """CarModelInline Admin StackedInline Class"""
    model = CarMake
    inline = [2]


class CarModelAdmin(admin.ModelAdmin):
    """CarModelAdmin Admin Model Class"""
    fields = ['name', 'type', 'year', 'mileage', 'car_make']


class CarMakeAdmin(admin.ModelAdmin):
    """CarMakeAdmin Admin Model Class"""
    fields = ['name', 'description']


admin.site.register(CarMake)
admin.site.register(CarModel)
