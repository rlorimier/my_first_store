from django.shortcuts import render, redirect


def view_bag(request):
    """ A view that renders the bag content page """

    return render(request, 'bag/bag.html')


# We'll submit the form to this view including the product id and the quantity
def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    # Once in the view we'll get the bag variable if it exists in the session or create it if it doesn't.
    bag = request.session.get('bag', {})

    # finally we'll add the item to the bag or update the quantity if it already exists.
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    # then overwrite the variable in the session with the updated version and then redirect the user back to the redirect URL.
    request.session['bag'] = bag
    return redirect(redirect_url)
