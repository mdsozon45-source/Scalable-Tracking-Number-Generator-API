import random
import string
from .models import TrackingNumber


def generate_tracking_number():
    while True:
        tracking_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        
        if not TrackingNumber.objects.filter(tracking_number=tracking_number).exists():
            return tracking_number
