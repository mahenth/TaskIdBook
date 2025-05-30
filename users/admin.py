from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile
from bookings.models import Booking

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('email', 'username', 'is_staff', 'is_active', 'total_bookings_admin')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

    # Custom method for total bookings in admin list display
    def total_bookings_admin(self, obj):
        return obj.bookings.count()
    total_bookings_admin.short_description = 'Total Bookings'

    # Filter by date range for total bookings (example - requires custom admin view or filter)
    # This is more complex for a simple `list_display` and would ideally be a custom admin report.
    # For a simple count, the method above is sufficient.
    # If a date range is needed, you'd implement a custom admin action or a separate view.

admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'gender')
    search_fields = ('user__email', 'address')