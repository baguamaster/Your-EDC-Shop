# cart views.py
from django.shortcuts import (render,
                              redirect,
                              reverse,
                              get_object_or_404)
from django.contrib import messages
from products.models import Product
from products.views import show_products
# Create your views here.


def view_cart(request):

    cart = request.session.get('shopping_cart', {})

    cart_total = 0

    # generate cart total
    for product_id in cart:
        cart_total = round(
            float(cart[product_id]['total_price']), 2) + cart_total

    return render(request, 'cart/view_cart-template.html', {
        'cart': cart,
        'cart_total': cart_total
    })


def add_to_cart(request, product_id):

    # retrieve shopping cart from session
    # {} is the default value if the shopping_cart is not found
    cart = request.session.get('shopping_cart', {})

    # get instance of the book model
    # criteria is product_id
    product = get_object_or_404(Product, pk=product_id)

    if product.quantity < 1:
        messages.error(request, f"Sorry! This item is no longer in stock")
        return(redirect(reverse(show_products)))

    if product_id in cart:
        cart[product_id]['qty'] += 1
        cart[product_id]['total_price'] = round(float(
            cart[product_id]['price']) * int(cart[product_id]['qty']), 2)

        product.quantity = product.quantity - 1
        product.save()

    # create cart dictionary with product_id as the key
    else:
        cart[product_id] = {
            # another dictionary
            'id': product_id,
            'name': product.name,
            'image': product.image.cdn_url,
            'price': round(float(product.price), 2),
            'total_price': round(float(product.price), 2),
            'qty': 1
        }
        # reduce quantity
        product.quantity = product.quantity - 1
        product.save()

    # save the shopping cart
    request.session['shopping_cart'] = cart

    messages.success(request, (str(product.name) +
                               " has been added to your cart"))
    return redirect(reverse('show_product_route'))


def remove_from_cart(request, product_id):
    # get cart from session
    cart = request.session.get('shopping_cart', {})
    product = get_object_or_404(Product, pk=product_id)

    if product_id in cart:

        # how much is in the cart?
        qty_in_cart = cart[product_id]['qty']

        # delete key from cart
        del cart[product_id]
        # save cart back into session
        request.session['shopping_cart'] = cart

        # update quantity
        product.quantity = product.quantity + qty_in_cart
        product.save()

        messages.success(request, (str(product.name) +
                                   " has been removed from your cart"))

    return redirect(reverse('show_product_route'))


def update_item_quantity(request, product_id):

    # get cart from session
    cart = request.session.get('shopping_cart', {})
    product = get_object_or_404(Product, pk=product_id)

    if product_id in cart:
        # check if update form is giving zero qty
        # zero quantity means removing item from cart
        if int(request.POST['qty']) == 0:
            messages.error(
                request, f"You cannot have enter a value of zero for quantity. Please remove the item from the cart if you wish to delete it.")
            return(redirect(reverse(view_cart)))

        # check qty
        eligible_stock = product.quantity
        incremental_added_to_cart = (
            int(request.POST['qty']) - cart[product_id]['qty'])
        if incremental_added_to_cart > eligible_stock:
            messages.error(request, f"Exceeded available stock")
            return(redirect(reverse(view_cart)))
        elif incremental_added_to_cart <= eligible_stock:
            # replace the qty under the product id key with the name="qty"
            # from request.POST
            cart[product_id]['qty'] = int(request.POST['qty'])
            cart[product_id]['total_price'] = round(float(
                cart[product_id]['price']) * int(request.POST['qty']), 2)
            request.session['shopping_cart'] = cart

            # update inventory
            product.quantity = product.quantity - incremental_added_to_cart
            product.save()

            messages.success(request, (str(product.name) +
                                       " quantity has been updated"))

    return redirect(reverse('view_cart'))
