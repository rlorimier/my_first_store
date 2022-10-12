"""
it will handle the bag items variable. Inside this file, I'm going to create a function called bag_contents.
Which will take the request as a parameter. Instead of returning a template though this function will return a dictionary
called context which were about to create. This is what's known as a context processor.
And its purpose is to make this dictionary available to all templates across the entire application
Much like you can use request.user in any template due to the presence of the built-in request context processor.
In order to make this context processor available to the entire application 
we need to add it to the list of context processors in the templates variable in settings.py
"""

from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):

    # First let's create an empty list for the bag items to live in. I'll also eventually need the total and 
    # the product count when we start adding things to the bag. So I'll initialize those now to zero
    bag_itens = []
    total = 0
    product_count = 0
    # Accessing the shopping bag, getting it if it already exists. Or initializing it to an empty dictionary if not
    bag = request.session.get('bag', {})

    # We need to iterate through all the items in the shopping bag. And along the way, tally up the total cost and product count.
    # And add the products and their data to the bag items list so we can display them on the shopping bag page and elsewhere throughout the site.
    for item_id, item_data in bag.items():
        #Now we only want to execute this code if the item has no sizes. If it's an integer then we know the item data is just the quantity.
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_itens.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        # we'll actually need to iterate through the inner dictionary of items_by_size incrementing the product count and total accordingly.
        # And also for each of these items, we'll add the size to the bag items returned to the template as well.
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_itens.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })


    # in order to entice customers to purchase more. We're going to give them free delivery if they spend more than the amount
    # specified in the free delivery threshold in settings.py
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE/100)

        # let's also let the user know how much more they need to spend
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        # If the total is greater than or equal to the threshold let's set delivery and the free_delivery_delta to zero
        delivery = 0
        free_delivery_delta = 0
    
    # to calculate the grand total. All I need to do is add the delivery charge to the total
    grand_total = delivery + total

    # we just need to add all these items to the context. So they'll be available in templates across the site
    context = {
        'bag_itens': bag_itens,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
