from django.db import models
import uuid


class Country(models.Model):
    country_code = models.CharField(max_length=2, unique=True)  
    country_name = models.CharField(max_length=100)

    def __str__(self):
        return self.country_name


class Customer(models.Model):
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=255)
    customer_slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name


class TrackingNumber(models.Model):
    tracking_number = models.CharField(max_length=16, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.tracking_number


class Parcel(models.Model):
    parcel_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    weight = models.DecimalField(max_digits=6, decimal_places=3)  
    origin_country = models.ForeignKey(Country, related_name="origin_country", on_delete=models.CASCADE)
    destination_country = models.ForeignKey(Country, related_name="destination_country", on_delete=models.CASCADE)
    tracking_number = models.OneToOneField(TrackingNumber, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Parcel ID: {self.parcel_id} | Tracking: {self.tracking_number}"


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    parcel = models.OneToOneField(Parcel, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=50, default="Pending")  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} | Customer: {self.customer.customer_name}"
