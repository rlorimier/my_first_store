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


def bag_contents(request):

    """First let's create an empty list for the bag items to live in. I'll also eventually need the total and 
    the product count when we start adding things to the bag. So I'll initialize those now to zero."""
    bag_itens = []
    total = 0
    product_count = 0

    """ in order to entice customers to purchase more. We're going to give them free delivery if they spend more than the amount 
    specified in the free delivery threshold in settings.py."""
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE/100)

        """let's also let the user know how much more they need to spend"""
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        """If the total is greater than or equal to the threshold let's set delivery and the free_delivery_delta to zero."""
        delivery = 0
        free_delivery_delta = 0
    
    """to calculate the grand total. All I need to do is add the delivery charge to the total."""
    grand_total = delivery + total

    """we just need to add all these items to the context. So they'll be available in templates across the site."""
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
