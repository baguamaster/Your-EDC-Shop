# reviews views
from django.shortcuts import (render,
                              redirect,
                              reverse,
                              get_object_or_404)
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from products.models import Product
from django.contrib.auth.decorators import login_required
from products.views import show_products, view_product_details

# Create your views here.


def show_reviews(request):
    # validation of username
    if not request.user.username == ('admin'):
        messages.error(request, f"Access Denied")
        return redirect(reverse(show_products))

    reviews = Review.objects.all()
    return render(request, 'reviews/show-reviews.template.html', {
        'reviews': reviews
    })


@login_required
def create_reviews(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        create_review_form = ReviewForm(request.POST)

        if create_review_form.is_valid():
            review_created = create_review_form.save(commit=False)
            review_created.product = product
            review_created.owner = request.user
            review_created.save()
            messages.success(
                request, f"New review has been created.")
            return render(request, 'products/product-details.template.html', {
                'product': product
            })
    else:
        create_review_form = ReviewForm()
        return render(request, 'reviews/create-reviews.template.html', {
            'form': create_review_form,
            'product': product
        })
