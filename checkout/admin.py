from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):

    readonly_fields = ('order_number', 'date', 'total',)

    fields = ('order_number', 'date', 'first_name', 'last_name',
              'email', 'phone_number', 'country', 'postcode',
              'town_or_city', 'street_address1',
              'street_address2', 'county', 'total',)

    list_display = ('order_number', 'date', 'first_name',
                    'last_name', 'total',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
