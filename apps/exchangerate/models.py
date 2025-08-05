from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ExchangeRateLog(models.Model):
    base_currency = models.CharField(max_length=10)
    target_currency = models.CharField(max_length=10)
    rate = models.DecimalField(max_digits=12, decimal_places=6)
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.base_currency} → {self.target_currency} = {self.rate} at {self.fetched_at}"
    
class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    duration_days = models.IntegerField(default=30)

    def __str__(self):
        return self.name
    
class Subscription(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    