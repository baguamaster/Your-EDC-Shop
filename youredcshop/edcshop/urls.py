from django.contrib import admin
from django.urls import path, include
import products.views

urlpatterns = [
    path('', products.views.landing_page, name="landing_page_route"),
    path('success', products.views.landing_page, name="landing_page_route"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('products/', include('products.urls')),
    path('reviews/', include('reviews.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls'))
]