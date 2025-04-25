from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Perfume(models.Model):
    CATEGORY_CHOICES = [
        ('sweet', 'Сладкие'),
        ('fresh', 'Свежие'),
        ('marine', 'Морские'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfumes')
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='perfumes/')

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def total_price(self):
        total = sum(item.quantity * item.perfume.price for item in self.items.all())
        if self.total_items() >= 20:
            total *= 0.9  # скидка 10%
        return round(total, 2)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
