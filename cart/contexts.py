def cart_contents(request):
    # retrieve shopping cart from session
    cart = request.session.get('shopping_cart', {})
    return {
        'shopping_cart': cart,
        'items_in_cart': len(cart)
    }
