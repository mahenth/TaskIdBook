from rest_framework import serializers
from .models import User, UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        return token
    
class UserProfileNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'address', 'photo', 'gender')
        read_only_fields = ('id',) # Make ID read-only if it's created automatically

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileNestedSerializer(read_only=True) # Add this line

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile') # Include 'profile'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # Assuming UserProfile is always created here, its ID will be in user.profile.id
        UserProfile.objects.create(user=user)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'address', 'photo', 'gender')

class UserProfileDetailSerializer(serializers.ModelSerializer):
    total_bookings = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('id', 'address', 'photo', 'gender', 'total_bookings')

    def get_total_bookings(self, obj):
        # This will be overridden in the viewset for date range filtering
        return 0

class AdminUserBookingSummarySerializer(serializers.Serializer):
    user_id = serializers.IntegerField(source='id')
    username = serializers.CharField()
    email = serializers.EmailField()
    total_bookings = serializers.IntegerField() # This will hold the annotated count
