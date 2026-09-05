from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Package, Subscription, Payment
from datetime import datetime
from dateutil.relativedelta import relativedelta

def packages(request):
    packages_list = Package.objects.filter(active=True).order_by('price')
    return render(request, 'billing/packages.html', {'packages': packages_list})

@login_required
def purchase_custom(request):
    if request.method == 'POST':
        speed = int(request.POST.get('speed', 10))
        price = int(request.POST.get('price', 1500))
        
        package_name = f"Custom Package ({speed} Mbps)"
        package, created = Package.objects.get_or_create(
            name=package_name,
            speed_mbps=speed,
            price=price,
            defaults={'active': False}
        )
        return redirect('purchase', pkg_id=package.id)
    return redirect('packages')

@login_required
def purchase(request, pkg_id):
    package = get_object_or_404(Package, id=pkg_id)
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except:
            start_date = datetime.today().date()
        
        # Create subscription (inactive initially)
        sub = Subscription(
            user=request.user,
            package=package,
            start_date=start_date,
            active=False
        )
        sub.save() # This triggers the custom save method to calculate expiry_date
        return redirect('payment', sub_id=sub.id)
        
    today = datetime.today().date()
    next_month = today + relativedelta(months=1)
    expiry = next_month.replace(day=8)
    return render(request, 'billing/purchase.html', {
        'package': package,
        'today': today.strftime('%Y-%m-%d'),
        'expiry_estimate': expiry.strftime('%b %d, %Y')
    })

@login_required
def payment(request, sub_id):
    sub = get_object_or_404(Subscription, id=sub_id, user=request.user)
    
    outstanding = request.user.userprofile.outstanding_balance
    total_amount = sub.package.price + outstanding

    if request.method == 'POST':
        trx_id = request.POST.get('transaction_id')
        receipt = request.FILES.get('receipt_image')
        Payment.objects.create(
            subscription=sub,
            amount=total_amount,
            outstanding_balance_paid=outstanding,
            transaction_id=trx_id,
            receipt_image=receipt,
            status='Pending'
        )
        messages.success(request, 'Payment submitted successfully. It is under verification.')
        return redirect('dashboard')
        
    return render(request, 'billing/payment.html', {
        'sub': sub,
        'outstanding': outstanding,
        'total_amount': total_amount
    })

@login_required
def track(request):
    payments_list = Payment.objects.filter(subscription__user=request.user).order_by('-created_at')
    return render(request, 'billing/track.html', {'payments': payments_list})

@login_required
def download_receipt(request, payment_id):
    payment_obj = get_object_or_404(Payment, id=payment_id, subscription__user=request.user)
    
    # Generate PDF using WeasyPrint
    from django.template.loader import render_to_string
    from weasyprint import HTML
    
    html_string = render_to_string('billing/receipt_pdf.html', {'payment': payment_obj})
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    pdf = html.write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{payment_obj.id}.pdf"'
    return response
