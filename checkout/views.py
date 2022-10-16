from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    #I'll get the bag from the session. And if there's nothing in the bag just add a simple error message.
    #And redirect back to the products page. This will prevent people from manually accessing the URL by typing /checkout
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51LsuJlBUscwmRijaGZQKXuciBbKIhuxOrR945pm32eeKktaX4UcWMTs179LbTOSYthe7Tg1miGKVmIsOEvVSK1Mm00jb4s8D7F',
        'client_secret': 'test client secret'
    }

    return render(request, template, context)
