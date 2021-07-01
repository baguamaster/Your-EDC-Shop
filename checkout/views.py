from django.shortcuts import (render,
                              reverse,
                              redirect,
                              HttpResponse,
                              get_object_or_404)
# import settings to access the public stripe key
from django.conf import settings
import stripe
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from products.models import Product
from checkout.models import Purchase
from django.views.decorators.csrf import csrf_exempt
from products.views import show_products
from cart.views import view_cart
from .forms import AddressForm

# Create your views here.


@login_required
def create_address(request):
    cart = request.session.get('shopping_cart', {})
    if (len(cart) == 0):
        messages.error(request, f"Fill up your cart first!")
        return(redirect(reverse(view_cart)))

    if request.method == 'POST':
        create_address_form = AddressForm(request.POST)

        if create_address_form.is_valid():
            address_created = create_address_form.save(commit=False)
            address_created.user_id = request.user
            create_address_form.save()
            messages.success(
                request,
                f"Your delivery details have been saved")
            return redirect(reverse(checkout))
        else:
            messages.error(
                request,
                f"Invalid Address Field")
            return render(request, 'checkout/create_address-template.html', {
                'form': create_address_form
            })

    else:
        create_address_form = AddressForm()
        return render(request, 'checkout/create_address-template.html', {
            'form': create_address_form
        })


@login_required
def checkout(request):
    cart = request.session.get('shopping_cart', {})
    if (len(cart) == 0):
        messages.error(request, f"Fill up your cart first!")
        return(redirect(reverse(view_cart)))
    else:
        # STRIP SECRET KEY!!
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # get shopping cart
        cart = request.session.get('shopping_cart', {})

        # create line items for checkout
        line_items = []

        # for storing the quantity of reach product
        all_product_ids = []

        for product_id, product in cart.items():
            # retrieve the book by its id from the database
            product_model = get_object_or_404(Product, pk=product_id)

            # create line item
            line_item = {
                "name": product_model.name,
                "amount": int(product_model.price * 100),
                "quantity": product['qty'],
                "currency": "SGD"
            }

            line_items.append(line_item)

            all_product_ids.append({
                'product_id': product_id,
                'qty': product['qty']
            })

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            client_reference_id=request.user.id,
            metadata={
                "all_product_ids": json.dumps(all_product_ids)
            },
            mode="payment",
            success_url=settings.STRIPE_SUCCESS_URL,
            cancel_url=settings.STRIPE_CANCEL_URL
        )

        # empty the shopping cart
        # request.session['shopping_cart'] = {}

        return render(request, 'checkout/checkout-template.html', {
            'session_id': session.id,
            'public_key': settings.STRIPE_PUBLISHABLE_KEY
        })


def checkout_success(request):
    # Empty the shopping cart
    request.session['shopping_cart'] = {}
    return render(request, 'checkout/checkout_success-template.html')


def checkout_cancelled(request):
    return render(request, 'checkout/checkout_cancelled-template.html')


# exempt from CSRF so that stripe can call our endpoint
@csrf_exempt
def payment_completed(request):
    # verify that request is truly from stripe
    payload = request.body

    # extract signature
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    # this prepares the variable to store data that stripe is sending
    event = None

    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature - what if data is not from stripe
        return HttpResponse(status=400)

    # data extraction only if STRIP clears
    # check if the event type is checkout.session.completed
    if event['type'] == 'checkout.session.completed':

        # if yes, then event represents that payment session is completed
        session = event['data']['object']

        # call handle_payment function to handle the payment complete
        handle_payment(session)

    return HttpResponse(status=200)


def handle_payment(session):
    user = get_object_or_404(User, pk=session["client_reference_id"])

    # change the metadata from string back to array
    all_product_ids_str = session["metadata"]["all_product_ids"]
    all_product_ids = json.loads(all_product_ids_str)

    # go through each book id
    # set counter
    count = -1
    # loop through all product_ids:
    for x in all_product_ids:
        count += 1
        product_id = all_product_ids[count]['product_id']
        qty = all_product_ids[count]['qty']

        product_model = get_object_or_404(Product, pk=product_id)

        # create the purchase model
        purchase = Purchase()
        purchase.product_id = product_model
        purchase.user_id = user
        purchase.price = product_model.price
        purchase.qty = qty
        purchase.save()


def show_purchases(request):
    # validation of username
    if not request.user.username == ('admin'):
        return redirect(reverse(show_products))

    purchases = Purchase.objects.all()
    return render(request, 'checkout/show_purchases-template.html', {
        'purchases': purchases
    })
