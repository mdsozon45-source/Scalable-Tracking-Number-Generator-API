from django.contrib import admin
from .models import Country, Customer, TrackingNumber, Parcel, Order

admin.site.register(Country)
admin.site.register(Customer)
admin.site.register(TrackingNumber)
admin.site.register(Parcel)
admin.site.register(Order)
