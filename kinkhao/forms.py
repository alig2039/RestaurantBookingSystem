import datetime
import time
from django.core.exceptions import ValidationError
from django.forms import modelform_factory
from django.forms import ModelForm
from kinkhao.models import *

# form classes and instances of forms shall be declared in this file

# instance to automatically make a form base on the ATable Model
TableForm = modelform_factory(Atable, exclude=[])
ResForm = modelform_factory(Bookings1, exclude=[])


class MyDateInput(forms.DateInput):
    """
    This is my widget for date input
    """
    input_type = 'date'


class CreateMealForm(forms.Form):
    theMealName = forms.CharField(required=True, max_length=30)
    theCuisineType = forms.ModelChoiceField(queryset=Cuisine.objects.all())


class CreateMealForm1(ModelForm):
    class Meta:
        model = Meal
        fields = ['mealName', 'cuisineType']


class TestTableForm1(ModelForm):
    restaurantLocation = forms.ModelChoiceField(queryset=RestaurantLocations.objects.all())
    tableNumber = forms.IntegerField(min_value=0, required=True)
    tableCapacity = forms.ModelChoiceField(queryset=TableCapacity.objects.all())

    class Meta:
        model = Atable
        fields = ['tableNumber', 'tableCapacity', 'restaurantLocation']

    def clean_tableNumber(self):
        data = self.cleaned_data['tableNumber']
        if 60 < data < 70:
            raise ValidationError("Those {} are too many tables".format(str(data)))
        if data > 100:
            raise ValidationError("This table Number figure {} is simple ridiculous".format(str(data)))

        return data


class TestTableForm(forms.Form):
    tableNumber = forms.IntegerField(min_value=0)
    tableCapacity = forms.ModelChoiceField(queryset=TableCapacity.objects.all())
    restLoc = forms.ModelChoiceField(label='Restaurant Location1',
                                     queryset=RestaurantLocations.objects.all())

    class Meta:
        model = Atable
        fields = '__all__'
        # fields = ['tableNumber', 'TableCapacity', 'restaurantLocation']
        field_classes = {
            'tableNumber': 'tableNumber',
            'TableCapacity': 'TableCapacity',
            'restaurantLocation': 'restLoc'
        }


class MakeReservationForm(ModelForm):
    contact_name = forms.CharField(label="Reservation Name",
                                   max_length=100,
                                   widget=forms.TextInput(attrs={"placeholder": "Enter your name"}))
    contact_email = forms.EmailField(label="Email", max_length=200,
                                     widget=forms.EmailInput(attrs={"placeholder": "Enter valid email"})
                                     )
    contact_phone = forms.CharField(label="Contact Phone", max_length=15, )
    # the_table = forms.IntegerField(label="Select capacity and location", min_value=1)
    the_table = forms.ModelChoiceField(label='Select a table',
                                       queryset=Atable.objects.all(),
                                       empty_label='select table details'
                                       )
    # restaurantLocation = forms.ModelChoiceField(label='Restaurant Location',
    #                                            queryset=RestaurantLocations.objects.all(),
    #
    #                                            )
    date = forms.DateField(label='Preferred date ', widget=MyDateInput)
    time_slot = forms.ModelChoiceField(label='Preferred time',
                                       queryset=TimeSlots.objects.all(),
                                       empty_label='select meal time',
                                       )

    class Meta:
        model = Bookings1
        fields = "__all__"

    def save(self,*args, **kwargs):
        try:
            result = super(self).save(*args, **kwargs)
        except InterruptedError as err:
            if (str(err)) == "Bookings1 with this The table, Time slot and Date already exists.":
                raise InterruptedError("Double booking")
            raise
        else:
            return result

    def clean_contact_phone(self):
        data = self.cleaned_data['contact_phone']
        # the statement below also works , however with get() a value get be supplied if the field is not found
        # .get("form field","default value incase form field is not found")
        # data1 = self.cleaned_data.get("contactPhone") also works
        minContactPhoneLength = 10

        # phone number should have at least 10 characters
        if len(data) < minContactPhoneLength:
            raise ValidationError(
                "Phone should be at least %s digits,you entered %s" % (minContactPhoneLength, len(data)))
        return data

    def clean_contact_name(self):
        data = self.cleaned_data['contact_name']
        # the contact name should not be less than 2 characters
        minContactNameLength = 2

        if len(" ".join(data.strip())) < minContactNameLength:
            raise ValidationError(
                "contact name should be at least %s characters,you entered %s" %
                (minContactNameLength, len(" ".join(data.strip()))))
        return data

    def clean_date(self):
        data = self.cleaned_data['date']
        if data < datetime.datetime.now().date():
            raise ValidationError("Date chosen is in the past choose again")

        return data

    # use this section to make sure that the date selected and time selected are not in the past
    def clean_time_slot(self):
        data = self.cleaned_data['time_slot']

        if datetime.datetime.strptime(str(data), "%H:%M:%S").time() < datetime.datetime.now().time():
            raise ValidationError(
                "time is in today's past"
            )
        return data
