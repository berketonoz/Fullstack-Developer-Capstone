"""admin.py import statements"""
from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    """CarModelInline Admin StackedInline Class"""
    model = CarMake
    inline  = [2]

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    """CarModelAdmin Admin Model Class"""
    fields = ['name', 'type', 'year', 'mileage', 'car_make']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    """CarMakeAdmin Admin Model Class"""
    fields = ['name', 'description']

# Register models here
admin.site.register(CarMake)
admin.site.register(CarModel)
