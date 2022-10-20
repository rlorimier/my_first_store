from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:

        """first we check whether sort is in request.get If it is. We set it equal to both sort which will be none at this point. And sortkey
        Then we rename sortkey to lower_name In the event, the user is sorting by name. Then we annotate the current list of products with a new field.
        And check whether the direction is descending in order to decide whether to reverse the order.
        Finally in order to actually sort the products all we need to do is use the order by model method."""   
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            """in order to allow case-insensitive sorting on the name field, we need to first annotate all the products with a new field.
            Annotation allows us to add a temporary field on a model """
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            """ in order to force categories to be sorted by name instead of their ids."""
            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        """ we'll check whether it exists in requests.get. If it does I'm gonna split it into a list at the commas.
        And then use that list to filter the current query set of all products down to only products whose category name is in the list. """
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        """ We can access those url parameters in the all_products view by checking whether request.get exists.
        Since we named the text input in the form q. We can just check if q is in request.get
        If it is I'll set it equal to a variable called query.
        If the query is blank it's not going to return any results. So if that's the case let's use
        the Django messages framework to attach an error message to the request. And then redirect back to the products url. """
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

    #The last thing I want to do is return the current sorting methodology to the template.
    current_sorting = f'{sort}_{direction}'
    
    context = {
        'products': products,
        # Now add the query to the context. And in the template call it search term.
        # Start with it as none at the top of this view to ensure we don't get an error when loading the products page without a search term.
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details  """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        # request.post and include request .files also In order to make sure to capture in the image of the product if one was submitted.
        form = ProductForm(request.POST, request.FILES)
        # simply check if form.is_valid. And if so we'll save it. Add a simple success message. And redirect to the same view.
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        # If there are any errors on the form We'll attach a generic error message telling the user to check their form which will display the errors.
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
