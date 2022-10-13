from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """ A view that renders the bag content page """

    return render(request, 'bag/bag.html')


# We'll submit the form to this view including the product id and the quantity
def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    # to add product sizes in the bag
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # Once in the view we'll get the bag variable if it exists in the session or create it if it doesn't.
    bag = request.session.get('bag', {})

    # I'll add an if statement to check if a product with sizes is being added.
    if size:
        # If the item is already in the bag. Then we need to check if another item of the same id and same size already exists.
         
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                # And if so increment the quantity for that size
                bag[item_id]['items_by_size'][size] += quantity
            else:
                # and otherwise just set it equal to the quantity.
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    #if there is no size
    else:
        # finally we'll add the item to the bag or update the quantity if it already exists.
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity
            # To add a message to the request object and use string formatting so the user know they added the product to the bag.
            messages.success(request, f'Added {product.name} to your bag')

    # then overwrite the variable in the session with the updated version and then redirect the user back to the redirect URL.
    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)