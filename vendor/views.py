
from django.db.models import Avg, F
from datetime import timezone
import functools
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from .models import HistoricalPerformance, PurchaseOrder, Vendor
from .serializers import HistoricalPerformanceSerializer, PurchaseOrderSerializer, VendorSerializer



@api_view(['GET', 'POST'])
def vendor_list(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET', 'PUT', 'DELETE'])
def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


# Purchase Order Views
@api_view(['GET', 'POST'])
def purchase_order_list(request):
    if request.method == 'GET':
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def purchase_order_detail(request, pu_id):
    po = get_object_or_404(PurchaseOrder, pk=pu_id)

    if request.method == 'GET':
        serializer = PurchaseOrderSerializer(po)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PurchaseOrderSerializer(po, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        po.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


# Historical Performance Views
@api_view(['GET'])
def historical_performance_list(request, vendor_id):
    performances = HistoricalPerformance.objects.filter(vendor=vendor_id)
    serializer = HistoricalPerformanceSerializer(performances, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def vendor_performance(request, vendor_id):
    # Retrieve the vendor
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    # Calculate on-time delivery rate
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', delivery_date__lte=timezone.now())
    total_completed_pos = completed_pos.count()
    on_time_delivery_rate = completed_pos.filter(delivery_date__lte=F('acknowledgment_date')).count() / total_completed_pos

    # Calculate quality rating average
    quality_rating_avg = PurchaseOrder.objects.filter(vendor=vendor, status='completed').aggregate(Avg('quality_rating'))['quality_rating__avg']

    # Calculate fulfillment rate
    total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfillment_rate = completed_pos.filter(issues__isnull=True).count() / total_pos

    # Return the performance metrics
    return Response({
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'fulfillment_rate': fulfillment_rate,
    })


@api_view(['POST'])
def acknowledge_purchase_order(request, po_id):
    # Retrieve the PO
    po = get_object_or_404(PurchaseOrder, pk=po_id)

    # Update acknowledgment_date
    po.acknowledgment_date = timezone.now()
    po.save()

    return Response({"message": "Acknowledgment successful"})