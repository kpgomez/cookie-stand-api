from django.contrib import admin
from .models import CookieStand


class CookieStandAdmin(admin.ModelAdmin):
    list_display = (
        "location",
        "owner",
        "description",
        "hourly_sales",
        "minimum_customers_per_hour",
        "maximum_customers_per_hour",
        "average_cookies_per_sale"
        # "created_at",
        # "updated_at",
    )


# Register your models here.
admin.site.register(CookieStand)
