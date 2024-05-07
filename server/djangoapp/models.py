"""models.py import statements"""
from django.db import models
# from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


class CarMake(models.Model):
    """CarMake Model For Django Application"""
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return str(self.name)


class CarModel(models.Model):
    """CarModel Model for Django Application"""
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('CONVERTIBLE', 'Convertible'),
        ('HATCHBACK', 'Hatchback'),
        ('COUPE', 'Coupe'),
        ('MINIVAN', 'Minivan'),
        ('PICKUP', 'Pickup'),
    ]
    type = models.CharField(
        max_length=11,
        choices=CAR_TYPES,
        default='SEDAN'
        )
    year = models.IntegerField(
        default=2024,
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(2024)
        ])
    # Other fields as needed
    mileage = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
            ])

    def __str__(self):
        return str(self.name)
