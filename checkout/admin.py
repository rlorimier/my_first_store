from django.contrib import admin
from .models import Order, OrderLineItem


# This inline item is going to allow us to add and edit line items in the admin right from inside the order model.
# So when we look at an order. We'll see a list of editable line items on the same page rather than having to go to the order line item interface.
class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    #These fields are things that will be calculated by our model methods
    # So we don't want anyone to have the ability to edit them since it could compromise the integrity of an order.
    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag',
                       'stripe_pid')

    #it will allow us to specify the order of the fields in the admin interface which would otherwise be adjusted by django due to the use of some read-only fields.
    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag',
              'stripe_pid')

    #I'll use the list display option. To restrict the columns that show up in the order list to only a few key items.
    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)
