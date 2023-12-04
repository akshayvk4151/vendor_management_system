from django.db.models.signals import post_save
from django.db.models import Avg, F
from django.dispatch import receiver
from .models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_average_response_time(sender, instance, **kwargs):
    if instance.acknowledgment_date:
        # Assuming you have a related Vendor field in PurchaseOrder named 'vendor'
        vendor = instance.vendor
        total_response_time = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).aggregate(Avg(F('acknowledgment_date') - F('issue_date')))['acknowledgment_date__avg']
        vendor.average_response_time = total_response_time
        vendor.save()