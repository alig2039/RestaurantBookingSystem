from django.contrib import admin

# This will import all the models
from .models import (RestaurantLocations,
                     TimeSlots,
                     TableCapacity,
                     Atable,
                     Cuisine,
                     Meal,
                     Bookings1,
                     )

# Register your models here.

# This will ensure that only those in this list will be registered in the admin site
models_list_register = [RestaurantLocations,
                        TimeSlots,
                        TableCapacity,
                        Atable,
                        Cuisine,
                        Meal,
                        Bookings1
                        ]

admin.site.register(models_list_register)
