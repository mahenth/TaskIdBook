from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'check_in_date', 'check_out_date', 'no_of_persons', 'created_at')
    list_filter = ('hotel', 'check_in_date', 'check_out_date')
    search_fields = ('user__email', 'hotel__name')
    date_hierarchy = 'check_in_date' 
    