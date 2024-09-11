from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, TrackingNumber, Parcel, Order, Country
from .serializers import TrackingNumberSerializer,CombinedCreateSerializer
from .utils import generate_tracking_number
from django.utils.dateparse import parse_datetime
from uuid import UUID
import uuid
import random
import string
from django.utils.text import slugify


class CombinedCreateAPIView(APIView):

    def generate_unique_slug(self, base_slug):
        slug = slugify(base_slug)
        unique_slug = slug
        num = 1
        while Customer.objects.filter(customer_slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def post(self, request):
        serializer = CombinedCreateSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            customer_id = data.get('customer_id')

            if customer_id:
                try:
                    customer = Customer.objects.get(customer_id=customer_id)
                except Customer.DoesNotExist:
                    return Response({"error": "Customer not found."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                customer_name = data.get('customer_name')
                
                base_slug = customer_name  
                customer_slug = self.generate_unique_slug(base_slug)

                customer = Customer.objects.create(
                    customer_name=customer_name,
                    customer_slug=customer_slug
                )

            tracking_number = generate_tracking_number()
            while TrackingNumber.objects.filter(tracking_number=tracking_number).exists():
                tracking_number = generate_tracking_number()

            tracking_instance = TrackingNumber.objects.create(
                tracking_number=tracking_number,
                customer=customer
            )

            origin_country = Country.objects.get(country_code=data['origin_country_id'])
            destination_country = Country.objects.get(country_code=data['destination_country_id'])
            parcel_instance = Parcel.objects.create(
                weight=data['weight'],
                origin_country=origin_country,
                destination_country=destination_country,
                tracking_number=tracking_instance
            )

            order_instance = Order.objects.create(
                customer=customer,
                parcel=parcel_instance,
                order_status=data['order_status']
            )

            response_data = {
                'customer_id': customer.customer_id,
                'customer_name': customer.customer_name,
                'customer_slug': customer.customer_slug,
                'tracking_number': tracking_instance.tracking_number,
                'parcel_id': parcel_instance.parcel_id,
                'order_id': order_instance.order_id,
                'order_status': order_instance.order_status,
                'created_at': order_instance.created_at
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class NextTrackingNumberAPIView(APIView):

    def generate_unique_slug(self, base_slug):
        slug = slugify(base_slug)
        unique_slug = slug
        num = 1
        while Customer.objects.filter(customer_slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def get(self, request, *args, **kwargs):
        
        origin_country_id = request.query_params.get('origin_country_id')
        destination_country_id = request.query_params.get('destination_country_id')
        weight = request.query_params.get('weight')
        created_at = request.query_params.get('created_at')
        customer_id = request.query_params.get('customer_id')
        customer_name = request.query_params.get('customer_name')
        customer_slug = request.query_params.get('customer_slug')

        if not all([origin_country_id, destination_country_id, weight, created_at]):
            return Response({"error": "All parameters except customer information are required."}, status=status.HTTP_400_BAD_REQUEST)

        if len(origin_country_id) != 2 or len(destination_country_id) != 2:
            return Response({"error": "Invalid country code format."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            weight = float(weight)
            if round(weight, 3) != weight:
                raise ValueError
        except ValueError:
            return Response({"error": "Invalid weight format. Must be a float with 3 decimal places."}, status=status.HTTP_400_BAD_REQUEST)


        if not parse_datetime(created_at):
            return Response({"error": "Invalid created_at timestamp."}, status=status.HTTP_400_BAD_REQUEST)

        if customer_id:
            try:
                UUID(customer_id)
            except ValueError:
                return Response({"error": "Invalid customer UUID."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                customer = Customer.objects.get(customer_id=customer_id)
            except Customer.DoesNotExist:
                return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        else:
            if not customer_name:
                return Response({"error": "Customer name is required when customer_id is not provided."}, status=status.HTTP_400_BAD_REQUEST)

            if not customer_slug:
                customer_slug = self.generate_unique_slug(customer_name)

       
            customer = Customer.objects.create(
                customer_name=customer_name,
                customer_slug=customer_slug
            )

        tracking_number = generate_tracking_number()

        tracking_entry = TrackingNumber.objects.create(
            tracking_number=tracking_number,
            customer=customer
        )

        serializer = TrackingNumberSerializer(tracking_entry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class CombinedDataSaveNextTrackingNumberAPIView(APIView):

    def generate_unique_slug(self, base_slug):
        slug = slugify(base_slug)
        unique_slug = slug
        num = 1
        while Customer.objects.filter(customer_slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def get(self, request, *args, **kwargs):
        origin_country_id = request.query_params.get('origin_country_id')
        destination_country_id = request.query_params.get('destination_country_id')
        weight = request.query_params.get('weight')
        created_at = request.query_params.get('created_at')
        customer_id = request.query_params.get('customer_id')
        customer_name = request.query_params.get('customer_name')
        customer_slug = request.query_params.get('customer_slug')

        if not all([origin_country_id, destination_country_id, weight, created_at]):
            return Response({"error": "All parameters except customer information are required."}, status=status.HTTP_400_BAD_REQUEST)

        if len(origin_country_id) != 2 or len(destination_country_id) != 2:
            return Response({"error": "Invalid country code format."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            weight = float(weight)
            if round(weight, 3) != weight:
                raise ValueError
        except ValueError:
            return Response({"error": "Invalid weight format. Must be a float with 3 decimal places."}, status=status.HTTP_400_BAD_REQUEST)

        if not parse_datetime(created_at):
            return Response({"error": "Invalid created_at timestamp."}, status=status.HTTP_400_BAD_REQUEST)

        if customer_id:
            try:
                UUID(customer_id)
            except ValueError:
                return Response({"error": "Invalid customer UUID."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                customer = Customer.objects.get(customer_id=customer_id)
            except Customer.DoesNotExist:
                return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        else:
            if not customer_name:
                return Response({"error": "Customer name is required when customer_id is not provided."}, status=status.HTTP_400_BAD_REQUEST)

            if not customer_slug:
                customer_slug = self.generate_unique_slug(customer_name)

            customer = Customer.objects.create(
                customer_name=customer_name,
                customer_slug=customer_slug
            )

        tracking_number = generate_tracking_number()

        tracking_entry = TrackingNumber.objects.create(
            tracking_number=tracking_number,
            customer=customer
        )

        try:
            origin_country = Country.objects.get(country_code=origin_country_id)
            destination_country = Country.objects.get(country_code=destination_country_id)
        except Country.DoesNotExist:
            return Response({"error": "One or both country codes are invalid."}, status=status.HTTP_400_BAD_REQUEST)

        parcel = Parcel.objects.create(
            weight=weight,
            origin_country=origin_country,
            destination_country=destination_country,
            tracking_number=tracking_entry
        )

        order = Order.objects.create(
            customer=customer,
            parcel=parcel,
            order_status='Pending'
        )

        response_data = {
            "tracking_number": tracking_entry.tracking_number,
            "customer": {
                "customer_id": customer.customer_id,
                "customer_name": customer.customer_name,
                "customer_slug": customer.customer_slug,
            },
            "parcel": {
                "parcel_id": parcel.parcel_id,
                "weight": parcel.weight,
                "origin_country": parcel.origin_country.country_code,
                "destination_country": parcel.destination_country.country_code
            },
            "order": {
                "order_id": order.order_id,
                "order_status": order.order_status,
                "created_at": order.created_at
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
