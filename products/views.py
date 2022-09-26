from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None

    """ We can access those url parameters in the all_products view by checking whether request.get exists.
    Since we named the text input in the form q. We can just check if q is in request.get
    If it is I'll set it equal to a variable called query.
    If the query is blank it's not going to return any results. So if that's the case let's use
    the Django messages framework to attach an error message to the request. And then redirect back to the products url. """
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            """In Jango if you use something like product.objects.filter In order to filter a list of products everything will be ended together.
            In the case of our queries that would mean that when a user submits a query.
            In order for it to match the term would have to appear in both the product name and the product description.
            Instead, we want to return results where the query was matched in either the product name or the description.
            In order to accomplish this or logic, we need to use Q"""
            
            """ a variable equal to a Q object. Where the name contains the query. Or the description contains the query.
            The pipe here is what generates the or statement. And the i in front of contains makes the queries case insensitive."""
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            # pass them to the filter method in order to actually filter the products.
            products = products.filter(queries)

    context = {
        'products': products,
        # Now add the query to the context. And in the template call it search term.
        # Start with it as none at the top of this view to ensure we don't get an error when loading the products page without a search term.
        'search_term': query,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details  """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
