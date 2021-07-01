from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.


class Address(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.PositiveIntegerField(blank=False)
    postal_code = models.PositiveIntegerField(blank=False)
    address = models.TextField(blank=False)

    def __str__(self):
        return self.address


class Purchase(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    qty = models.IntegerField(default=0)
    total = models.DecimalField(default=0, max_digits=19, decimal_places=2)
    price = models.DecimalField(default=0, max_digits=19, decimal_places=2)

    def __str__(self):
        return f"Purchase made for product#{self.product_id} by user#{self.user_id} on {self.purchase_date}"

    def save(self, *args, **kwargs):
        self.total = self.price * self.qty
        super().save(*args, **kwargs)