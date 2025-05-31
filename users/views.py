
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer, CustomTokenObtainPairSerializer, UserProfileDetailSerializer, AdminUserBookingSummarySerializer
from bookings.models import Booking # Import Booking model here
from rest_framework.decorators import action
from datetime import datetime
from rest_framework.permissions import IsAdminUser

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] # Allow any for signup

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated] # Restrict other actions after signup
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        # Handles signup
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see/edit their own profile
        return self.queryset.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserProfileDetailSerializer(instance) # Use the detail serializer for retrieve
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # Custom action to get total bookings in a date range for the user
    def get_serializer_class(self):
        if self.action == 'total_bookings_in_range':
            return UserProfileDetailSerializer # Can reuse or create a more specific one
        return super().get_serializer_class()

    @action(detail=True, methods=['get'])
    def total_bookings_in_range(self, request, pk=None):
        profile = self.get_object()
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        if not all([start_date_str, end_date_str]):
            return Response({"detail": "Please provide both 'start_date' and 'end_date' query parameters."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            from datetime import datetime
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)

        total_bookings = Booking.objects.filter(
            user=profile.user,
            check_in_date__range=[start_date, end_date]
        ).count()

        serializer = UserProfileDetailSerializer(profile)
        data = serializer.data
        data['total_bookings'] = total_bookings
        return Response(data)
    

class AdminBookingSummaryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser] # Only authenticated admins

    def list(self, request):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        if not all([start_date_str, end_date_str]):
            return Response({"detail": "Please provide both 'start_date' and 'end_date' query parameters (YYYY-MM-DD)."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Filter bookings by date range
        # Annotate users with the count of their bookings within that range
        # filter(bookings__isnull=False) ensures only users with bookings in the range are included
        users_with_bookings = User.objects.filter(
            bookings__check_in_date__range=[start_date, end_date]
        ).annotate(
            total_bookings=Count('bookings')
        ).order_by('id') # Order for consistent results

        serializer = AdminUserBookingSummarySerializer(users_with_bookings, many=True)
        return Response(serializer.data)
