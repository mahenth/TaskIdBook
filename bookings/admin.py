from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'check_in_date', 'check_out_date', 'no_of_persons', 'created_at')
    list_filter = ('hotel', 'check_in_date', 'check_out_date')
    search_fields = ('user__email', 'hotel__name')
    date_hierarchy = 'check_in_date' # Allows date-based drilldown

    # Admin should be able to get the total number of booking made by each user based on date (check in)
    # This requires a custom report or filtering on the admin page.
    # The `list_filter` with `check_in_date` already provides some basic filtering.
    # For a consolidated report, you'd likely create a custom admin view.