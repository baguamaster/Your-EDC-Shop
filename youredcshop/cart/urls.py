from django.urls import path
import cart.views

urlpatterns = [
    path('add/<product_id>', cart.views.add_to_cart, name='add_to_cart'),
    path('', cart.views.view_cart, name='view_cart'),
    path('remove/<product_id>', cart.views.remove_from_cart,
         name='remove_from_cart'),
    path('update/<product_id>', cart.views.update_item_quantity,
