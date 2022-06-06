from django.db import models
import datetime
from django import forms


# Create your models here.


class Days(models.Model):
    day = models.CharField(max_length=9, blank=False, unique=True)


class RestaurantLocations(models.Model):
    location = models.CharField(max_length=20, unique=True, null=False)

    # days = models.ManyToManyField(Days, through="RestaurantLocationsAndDays")

    # days = models.ManyToManyField(Days)

    # This will help display the actual location name in the drop down list of the admin site
    # so that is does not just display
    def __str__(self):
        return str(self.location)

    class Meta:
        verbose_name_plural = "Restaurant Locations"


class TableCapacity(models.Model):
    capacity = models.PositiveSmallIntegerField(unique=True, null=False)

    class Meta:
        verbose_name_plural = "Table Capacities"

    def __unicode__(self):
        return "Table Capacity"

    def __str__(self):
        return str(self.capacity)


class TimeSlots(models.Model):
    timeSlot = models.TimeField(unique=True, null=False)

    def __str__(self):
        return str(self.timeSlot)

    class Meta:
        verbose_name_plural = "Time slots"


class Atable(models.Model):
    tableNumber = models.PositiveSmallIntegerField(null=False)
    tableCapacity = models.ForeignKey(TableCapacity, to_field="capacity", on_delete=models.CASCADE)
    restaurantLocation = models.ForeignKey(RestaurantLocations, to_field="location", on_delete=models.CASCADE, )

    def __str__(self):
        location_tblNbr_tblCapacity = "{}, {} seater, table-{}".format(str(self.restaurantLocation),
                                                                       str(self.tableCapacity),
                                                                       str(self.tableNumber)
                                                                       )
        return location_tblNbr_tblCapacity

    class Meta:
        # more than one table at the same location cannot have the same table number
        constraints = [
            models.UniqueConstraint(name='Unique_tableNumber_at_restaurantLocation',
                                    fields=['restaurantLocation', 'tableNumber'])
        ]
        verbose_name_plural = "Tables"


class Cuisine(models.Model):
    cuisineName = models.CharField(max_length=20, null=False, unique=True)

    def __str__(self):
        return str(self.cuisineName)


class Meal(models.Model):
    mealName = models.CharField(max_length=30, null=False)
    cuisineType = models.ForeignKey(Cuisine, to_field="cuisineName", on_delete=models.PROTECT)

    def __str__(self):
        return str(self.mealName)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='Unique_mealName_and_cuisineType', fields=['mealName', 'cuisineType']
            )
        ]


class Bookings1(models.Model):
    contact_name = models.CharField(max_length=100, null=False)
    contact_email = models.EmailField(max_length=200, null=False)
    contact_phone = models.CharField(max_length=15, null=False)
    the_table = models.ForeignKey(Atable, on_delete=models.PROTECT)
    time_slot = models.ForeignKey(TimeSlots, on_delete=models.PROTECT)
    # day = models.ForeignKey(Days,to_field="day",on_delete=models.PROTECT,default="Saturday")
    date = models.DateField(null=False, default=datetime.date.today())

    class Meta:
        constraints = [models.UniqueConstraint(
            name='unique_table_location_timeSlot_date',
            fields=['the_table', 'time_slot', 'date']
        )

        ]




class RestaurantLocationsAndDays(models.Model):
    """
    This table/ models will list which days a particular location will offer services
    For example the Kampala location may offer
    """
    restaurantLocations = models.ForeignKey(RestaurantLocations, on_delete=models.CASCADE)
    days = models.ForeignKey(Days, on_delete=models.PROTECT)

    class Meta:
        # the combination of location and day should be unique
        constraints = [
            models.UniqueConstraint(name='Unique_restaurantLocation_on_day',
                                    fields=['restaurantLocations', 'days'])
        ]
