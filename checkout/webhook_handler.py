from django.http import HttpResponse


# Each time an event occurs on stripe such as a payment intent being created.
# A payment being completed and so on stripe sends out what's called a webhook we can listen for.
# Webhooks are like the signals django sends each time a model is saved or deleted.
# Except that they're sent securely from stripe to a URL we specify.
class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
