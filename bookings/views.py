from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Booking
from .serializers import BookingSerializer, BookingRetrieveSerializer
from datetime import datetime

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'check_in_date': ['gte', 'lte', 'range'], # For date range filtering
    }
    ordering_fields = ['check_in_date', 'created_at']

    def get_queryset(self):
        # Users can only see their own bookings
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookingRetrieveSerializer
        return BookingSerializer

    