from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class CarModel(models.Model):
    CAR_TYPES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Wagon', 'Wagon'),
        ('Crossover', 'Crossover'),
        ('Truck', 'Truck'),
        ('Coupe', 'Coupe'),
    ]
    
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CAR_TYPES, default='Sedan')
    year = models.IntegerField(
        default=2026,
        validators=[
            MaxValueValidator(2026),
            MinValueValidator(2015)
        ]
    )
    
    def __str__(self):
        return f"{self.car_make.name} {self.name}"
