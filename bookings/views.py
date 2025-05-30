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

    # Custom action for filtering bookings by date range for the current user
    # This is handled by `filterset_fields` and DjangoFilterBackend, but a custom action
    # could also be implemented if more complex logic is needed.
    # For example, if you wanted to pass "start_date" and "end_date" directly
    # and map them to `check_in_date__gte` and `check_in_date__lte` internally.
    #
    # @action(detail=False, methods=['get'])
    # def by_date_range(self, request):
    #     start_date_str = request.query_params.get('start_date')
    #     end_date_str = request.query_params.get('end_date')
    #
    #     if not all([start_date_str, end_date_str]):
    #         return Response({"detail": "Please provide both 'start_date' and 'end_date' query parameters."},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     try:
    #         start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    #         end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    #     except ValueError:
    #         return Response({"detail": "Invalid date format. Use YYYY-MM-DD."},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     queryset = self.get_queryset().filter(
    #         check_in_date__range=[start_date, end_date]
    #     )
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)