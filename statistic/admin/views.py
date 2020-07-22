# Python imports
from itertools import chain
import operator

# Django imports
from django.utils import timezone
from django.db.models import (
    Sum,
    F
)
from django.db import models

# Django REST framework imports
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import (
    APIView,
)
from rest_framework.exceptions import (
    ValidationError,
    AuthenticationFailed
)
from rest_framework.pagination import PageNumberPagination

# Application imports
from templates.error_template import (
    ErrorTemplate,
)
from api.permissions import (
    IsAdmin,
)

# Model imports
from goods_receipt.models import (
    GoodsReceipt
)
from order.models import Order
from order_detail.models import OrderDetail

# Serialier imports
from statistic.admin.serializers import (
    RevenueStatisticSerializer,
    FlowerStatisticSerializer
)

# List Revenue Statistic
class RevenueStatisticView(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request, *args, **kwargs):
        month__gte = self.request.GET.get('month__gte')
        month__lte = self.request.GET.get('month__lte')
        year__gte = self.request.GET.get('year__gte')
        year__lte = self.request.GET.get('year__lte')
        month__exact = self.request.GET.get('month__exact')
        year__exact = self.request.GET.get('year__exact')

        expenses = None
        incomes = None
        if month__exact and year__exact:
            expenses = GoodsReceipt.objects.filter(
                created_at__month__exact=month__exact,
                created_at__year__exact=year__exact,
            ).extra({
                'month': 'MONTH(created_at)', 
                'year': 'YEAR(created_at)'
            }).values(
                'month',
                'year'
            ).annotate(
                expenses_total=Sum(
                    F('historical_cost')*F('receipt_quantity'), 
                    output_field=models.DecimalField()
                )
            )
            incomes = Order.objects.filter(
                checkout=True,
                created_at__month__exact=month__exact,
                created_at__year__exact=year__exact,
            ).extra({
                'month': 'MONTH(created_at)',
                'year': 'YEAR(created_at)'
            }).values(
                'month',
                'year'
            ).annotate(
                total_revenue=Sum('total')
            )
        elif month__gte and month__lte and year__gte and year__lte:
            expenses = GoodsReceipt.objects.filter(
                created_at__month__gte=month__gte,
                created_at__month__lte=month__lte,
                created_at__year__gte=year__gte,
                created_at__year__lte=year__lte,
            ).extra({
                'month': 'MONTH(created_at)', 
                'year': 'YEAR(created_at)'
            }).values(
                'month',
                'year'
            ).annotate(
                expenses_total=Sum(
                    F('historical_cost')*F('receipt_quantity'), 
                    output_field=models.DecimalField()
                )
            )
            incomes = Order.objects.filter(
                checkout=True,
                created_at__month__gte=month__gte,
                created_at__month__lte=month__lte,
                created_at__year__gte=year__gte,
                created_at__year__lte=year__lte,
            ).extra({
                'month': 'MONTH(created_at)',
                'year': 'YEAR(created_at)'
            }).values(
                'month',
                'year'
            ).annotate(
                total_revenue=Sum('total')
            )
        else:
            expenses = GoodsReceipt.objects.all(
            ).extra({
                'month': 'MONTH(created_at)', 
                'year': 'YEAR(created_at)'
            }).values(
                'month',
                'year'
            ).annotate(
                expenses_total=Sum(
                    F('historical_cost')*F('receipt_quantity'), 
                    output_field=models.DecimalField()
                )
            )
            incomes = Order.objects.filter(
                checkout=True
            ).extra({
                'month': 'MONTH(created_at)',
                'year': 'YEAR(created_at)'
            }).values(
                'month',
                'year'
            ).annotate(
                total_revenue=Sum('total')
            )
        combined_queryset = list(chain(expenses, incomes))
        combined_queryset.sort(key=operator.itemgetter('year', 'month'))

        i = 0
        while i < len(combined_queryset)-1:
            current_record = combined_queryset[i]
            next_record = combined_queryset[i+1]

            # Check duplicate month and year            
            if current_record.get('month') == next_record.get('month') and current_record.get('year') == next_record.get('year'):
                if current_record.get('expenses_total'):
                    current_record['total_revenue'] = next_record.get('total_revenue')
                    combined_queryset.remove(next_record)
                elif current_record.get('total_revenue'):
                    current_record['expenses_total'] = next_record.get('expenses_total')
                    combined_queryset.remove(next_record)
            i += 1

        # Set empty fields = 0
        for record in combined_queryset:
            if not record.get('total_revenue'):
                record['total_revenue'] = 0
            if not record.get('expenses_total'):
                record['expenses_total'] = 0

            # Insert net_income
            record['net_income'] = record.get('total_revenue') - record.get('expenses_total')

        serializer = RevenueStatisticSerializer(combined_queryset, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        })

# List Flower Statistic
class FlowerStatisticView(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request, *args, **kwargs):
        month__gte = self.request.GET.get('month__gte')
        month__lte = self.request.GET.get('month__lte')
        year__gte = self.request.GET.get('year__gte')
        year__lte = self.request.GET.get('year__lte')
        month__exact = self.request.GET.get('month__exact')
        year__exact = self.request.GET.get('year__exact')

        orderdetails = None
        if month__exact and year__exact:
            orderdetails = OrderDetail.objects.filter(
                order__checkout=True,
                order__created_at__month__exact=month__exact,
                order__created_at__year__exact=year__exact,
            ).extra({
                'month': 'MONTH(order.created_at)', 
                'year': 'YEAR(order.created_at)'
            }).values(
                'month', 
                'year',
                'flower__name'
            ).annotate(
                total_quantity=Sum('quantity')
            )
        elif month__gte and month__lte and year__gte and year__lte:
            orderdetails = OrderDetail.objects.filter(
                order__checkout=True,
                order__created_at__month__gte=month__gte,
                order__created_at__month__lte=month__lte,
                order__created_at__year__gte=year__gte,
                order__created_at__year__lte=year__lte,
            ).extra({
                'month': 'MONTH(order.created_at)', 
                'year': 'YEAR(order.created_at)'
            }).values(
                'month', 
                'year',
                'flower__name'
            ).annotate(
                total_quantity=Sum('quantity')
            )
        else:
            orderdetails = OrderDetail.objects.filter(
                order__checkout=True
            ).extra({
                'month': 'MONTH(order.created_at)', 
                'year': 'YEAR(order.created_at)'
            }).values(
                'month', 
                'year',
                'flower__name'
            ).annotate(
                total_quantity=Sum('quantity')
            )
        serializer = FlowerStatisticSerializer(orderdetails, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        })




