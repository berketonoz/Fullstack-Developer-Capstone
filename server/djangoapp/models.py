# Uncomment the following imports before adding the Model code

from django.db import models
# from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


class CarMake(models.Model): 
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Other fields as needed

    def __str__(self): 
        return self.name  # Return the name as the string representation


class CarModel(models.Model): 
    # Many-to-One relationship
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    CAR_TYPES = [
        ('SEDAN','Sedan'), 
        ('SUV','SUV'), 
        ('CONVERTIBLE','Convertible'), 
        ('HATCHBACK','Hatchback'), 
        ('COUPE','Coupe'), 
        ('MINIVAN','Minivan'), 
        ('PICKUP','Pickup'), 
    ]
    type = models.CharField(max_length=11, choices=CAR_TYPES, default='SEDAN')
    year = models.IntegerField(default=2024,
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(2024)
        ])
    # Other fields as needed

    def __str__(self): 
        return self.name  # Return the name as the string representation
    