# products views.py
from django.shortcuts import (render,
                              redirect,
                              reverse,
                              get_object_or_404)
from django.contrib import messages
from django.db.models import Q
from .models import Product
from .forms import ProductForm, SearchForm

# Create your views here.


def landing_page(request):
    return render(request, 'products/landing_page-template.html')


def show_products(request):
    search_form = SearchForm(request.GET)
    products = Product.objects.all()

    query = ~Q(pk__in=[])

    # check if product type exist, and is not empty
    if 'name' in request.GET and request.GET['name']:
        query = query & Q(name__icontains=request.GET['name'])

    # check if product type exist, and is not empty
    if 'product_type' in request.GET and request.GET['product_type']:
        query = query & Q(product_type__exact=request.GET['product_type'])

    # Only assign distinct values
    products = products.filter(query).distinct()

    return render(request, 'products/show_products-template.html', {
        'products': products,
        'search_form': search_form
    })


# view product details
def view_product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_details-template.html', {
        'product': product
    })


def create_product(request):
    # validation of username
    if not request.user.username == ('admin'):
        messages.error(request, f"Access Denied")
        return redirect(reverse(show_products))

    if request.method == 'POST':
        create_product_form = ProductForm(request.POST)

        if create_product_form.is_valid():
            create_product_form.save()
            messages.success(
                request,
                f"New product {create_product_form.cleaned_data['name']} has been created")
            return redirect(reverse(show_products))
        else:
            return render(request, 'products/create_products-template.html', {
                'form': create_product_form
            })

    else:
        create_product_form = ProductForm()
        return render(request, 'products/create_products-template.html', {
            'form': create_product_form
        })


def update_product(request, product_id):
    # validation of username
    if not request.user.username == ('admin'):
        messages.error(request, f"Access Denied")
        return redirect(reverse(show_products))

    # Get product to be updated from db
    product_being_updated = get_object_or_404(Product, pk=product_id)

    # check if the update form is submitted
    if request.method == "POST":
        # get values from the POST method
        product_update_form = ProductForm(
            request.POST, instance=product_being_updated)

        # check if the value of the form is valid
        if product_update_form.is_valid():
            # if yes, save and redirect to product listings
            product_update_form.save()
            return redirect(reverse(show_products))
        else:
            # re-render the form with values from POST, but don't save yet
            return render(request, 'products/update_product-template.html', {
                "form": product_update_form
            })

    else:
        # if not POST, then just render the form with product_id instance
        update_product_form = ProductForm(instance=product_being_updated)
        return render(request, 'products/update_product-template.html', {
            "product_being_updated": product_being_updated,
            "form": update_product_form
        })


def delete_product(request, product_id):
    # validation of username
    if not request.user.username == ('admin'):
        messages.error(request, f"Access Denied")
        return redirect(reverse(show_products))

    product_to_delete = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product_to_delete.delete()
        messages.success(
            request,
            f"Product has been deleted")
        return redirect(reverse(show_products))
    else:
        return render(request, 'products/delete_product-template.html', {
            "product": product_to_delete
        })
