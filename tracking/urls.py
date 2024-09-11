from django.urls import path
from .views import NextTrackingNumberAPIView,CombinedCreateAPIView,CombinedDataSaveNextTrackingNumberAPIView

urlpatterns = [
    path('create-order/', CombinedCreateAPIView.as_view(), name='create_order'),
    path('next-tracking-number/', NextTrackingNumberAPIView.as_view(), name='next-tracking-number'),
    path('combined-next-tracking-number/', CombinedDataSaveNextTrackingNumberAPIView.as_view(), name='combined-next-tracking-number'),
]
