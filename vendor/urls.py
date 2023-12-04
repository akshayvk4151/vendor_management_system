from django.urls import path
from .views import acknowledge_purchase_order, historical_performance_list, purchase_order_detail, purchase_order_list, vendor_list,vendor_detail, vendor_performance

urlpatterns = [
    path('api/vendors/', vendor_list, name='vendor-list'),
    path('api/vendors/<int:vendor_id>/', vendor_detail, name='vendor-detail'),
    path('api/purchase_orders/', purchase_order_list, name='purchase-order-list'),
    path('api/purchase_orders/<int:pu_id>/', purchase_order_detail, name='purchase-order-detail'),
    path('api/vendors/<int:vendor_id>/historical_performance/', historical_performance_list, name='historical-performance-list'),
    path('api/vendors/<int:vendor_id>/performance/', vendor_performance, name='vendor-performance'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', acknowledge_purchase_order, name='acknowledge-purchase-order'),
]