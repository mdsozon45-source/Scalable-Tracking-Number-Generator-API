from rest_framework import serializers
from .models import Country, Customer, TrackingNumber, Parcel, Order
import uuid

class CombinedCreateSerializer(serializers.Serializer):
    customer_id = serializers.UUIDField(required=False, allow_null=True)
    customer_name = serializers.CharField(required=False, allow_blank=True)
    customer_slug = serializers.SlugField(required=False, allow_blank=True)
    weight = serializers.DecimalField(max_digits=6, decimal_places=3)
    origin_country_id = serializers.CharField(max_length=2)
    destination_country_id = serializers.CharField(max_length=2)
    order_status = serializers.CharField(max_length=50)
    
    def validate(self, data):
        if not data.get('customer_id'):
            if not data.get('customer_name'):
                raise serializers.ValidationError({'customer_name': 'This field is required.'})
            
        return data

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_code', 'country_name']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'customer_name', 'customer_slug', 'created_at']

class TrackingNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingNumber
        fields = ['tracking_number', 'created_at', 'customer']

class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ['parcel_id', 'weight', 'origin_country', 'destination_country', 'tracking_number', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'customer', 'parcel', 'order_status', 'created_at']
