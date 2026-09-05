from django.urls import path
from . import views

urlpatterns = [
    path('packages/', views.packages, name='packages'),
    path('purchase/custom/', views.purchase_custom, name='purchase_custom'),
    path('purchase/<int:pkg_id>/', views.purchase, name='purchase'),
    path('payment/<int:sub_id>/', views.payment, name='payment'),
    path('track/', views.track, name='track'),
    path('receipt/<int:payment_id>/pdf/', views.download_receipt, name='download_receipt'),
]
