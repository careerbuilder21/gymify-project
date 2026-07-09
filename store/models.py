from django.db import models
from members.models import Member

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('energy',     'Energy Drink'),
        ('preworkout', 'Pre-Workout'),
        ('protein',    'Protein'),
        ('bcaa',       'BCAA'),
    ]
    name        = models.CharField(max_length=200)
    description = models.TextField()
    category    = models.CharField(
                      max_length=15,
                      choices=CATEGORY_CHOICES)
    price       = models.DecimalField(
                      max_digits=8,
                      decimal_places=2)
    stock       = models.IntegerField(default=0)
    image       = models.ImageField(
                      upload_to='products/',
                      blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
    ]
    member          = models.ForeignKey(
                          Member,
                          on_delete=models.CASCADE,
                          null=True)
    total_amount    = models.DecimalField(
                          max_digits=10,
                          decimal_places=2,
                          default=0)
    payment_method  = models.CharField(
                          max_length=20,
                          choices=PAYMENT_CHOICES,
                          default='bank_transfer')
    status          = models.CharField(
                          max_length=20,
                          default='pending')
    order_date      = models.DateTimeField(
                          auto_now_add=True)

    # Bank Transfer Fields
    bank_name       = models.CharField(
                          max_length=50,
                          blank=True)
    account_title   = models.CharField(
                          max_length=100,
                          blank=True)
    account_number  = models.CharField(
                          max_length=50,
                          blank=True)
    transaction_ref = models.CharField(
                          max_length=100,
                          blank=True)
    transfer_amount = models.DecimalField(
                          max_digits=10,
                          decimal_places=2,
                          default=0)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order    = models.ForeignKey(
                   Order,
                   on_delete=models.CASCADE)
    product  = models.ForeignKey(
                   Product,
                   on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price    = models.DecimalField(
                   max_digits=8,
                   decimal_places=2)

    def __str__(self):
        return f"{self.product} x {self.quantity}"