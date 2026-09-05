from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

class Package(models.Model):
    name = models.CharField(max_length=100)
    speed_mbps = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.speed_mbps} Mbps)"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    start_date = models.DateField(default=date.today)
    expiry_date = models.DateField()
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expiry_date:
            next_month = self.start_date + relativedelta(months=1)
            self.expiry_date = next_month.replace(day=8)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.package.name}"

class Payment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending Verification'),
        ('Verified', 'Verified'),
        ('Rejected', 'Rejected'),
    ]
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gateway = models.CharField(max_length=50, default='EasyPaisa')
    outstanding_balance_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subscription.user.username} - {self.amount} - {self.status}"
