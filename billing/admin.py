from django.contrib import admin
from .models import Package, Subscription, Payment

@admin.action(description="Verify selected payments")
def verify_payments(modeladmin, request, queryset):
    for payment in queryset:
        if payment.status == 'Pending':
            payment.status = 'Verified'
            payment.save()
            
            # Deduct outstanding balance if paid
            if payment.outstanding_balance_paid > 0:
                profile = payment.subscription.user.userprofile
                profile.outstanding_balance -= payment.outstanding_balance_paid
                if profile.outstanding_balance < 0:
                    profile.outstanding_balance = 0
                profile.save()

            # Activate subscription
            payment.subscription.active = True
            payment.subscription.save()

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('transaction_id', 'subscription__user__username')
    actions = [verify_payments]

class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'speed_mbps', 'price', 'active')

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'start_date', 'expiry_date', 'active')
    list_filter = ('active',)
    search_fields = ('user__username',)

admin.site.register(Package, PackageAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Payment, PaymentAdmin)
