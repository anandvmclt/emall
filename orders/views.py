#emall/orders/views.py
from django.db.models import Q
from functools import reduce
import operator
import logging
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from user.rbac import IsAdmin, IsGetOrAdmin, IsManager
from .models import Orders, OrderStatus
from rest_framework.views import APIView
from .serializers import OrdersSerializer,OrderDetailSerializer
# Create your views here.


logger = logging.getLogger("django")


def index(request):
    logger.info("Logger ok")
    logger.warning("Logger Warning")
    logger.debug("Logger Debug")
    return JsonResponse({"message": "Welcome !"})


# List and create new Orders
class OrdersListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Orders.objects.filter(is_deleted=False, status=True).order_by('id')
    serializer_class = OrdersSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['order_id', 'customer', 'order_status', 'uuid']

    def list(self, request, *args, **kwargs):
        
        try:
            user = self.request.user
            # access queryset from class level object
            queryset = self.get_queryset()
            filter_field = self.request.query_params.get('filter_field')  # Get the dynamic filter field
            filter_value = self.request.query_params.get('filter_value')  # Get the filter value


            if user.user_scope in ("MANAGER", "ADMIN"):
                queryset = queryset # No changes in query set for this condition
            else:
                 # added extra filter for queryset.
        
                 queryset = queryset.filter(**{'customer':user})
            

            # Filtering based on keys and values from request parameters
            if filter_field and filter_value:
                filter_args = {filter_field: filter_value}
                queryset = queryset.filter(**filter_args)


            # Accessing pagination class and generating paginated queryset
            page = self.paginate_queryset(queryset)

            if page is not None:
                # Generate Serialized data from query result if pagination, is applicable
                serializer = self.get_serializer(page, many=True)
                res_data = {
                    'count': self.paginator.count,
                    'next': self.paginator.get_next_link(),
                    'previous': self.paginator.get_previous_link(),
                    'results': serializer.data
                }
                return Response(res_data, status=status.HTTP_200_OK)

            # If paginator is not applicable return normal result
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Order Listing API : {e}")
            return Response("Something went wrong", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrdersDetailsAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsGetOrAdmin,)
    queryset = Orders.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = OrderDetailSerializer
    lookup_field = 'uuid'

    # Change Order status

    
class ChangeOrderStatusView(APIView):

    permission_classes =  (IsAuthenticated, IsManager | IsAdmin)

    def post(self, request, uuid):
      try:
        data = request.data
        new_status = data.get("order_status")
        # Check for valid order status submitted
        if new_status not in [choice[0] for choice in OrderStatus.ORDER_STATUS]:
            return Response({"status": False, "message": "Invalid Order Status", "data": OrderStatus.ORDER_STATUS},status=status.HTTP_400_BAD_REQUEST)

        # Find order object using uuid.
        order = Orders.objects.filter(uuid=uuid).first()
        if order:
            order.order_status = new_status
            order.save()
            return Response({"status": True, "message": "Updated Order Status", "data": {}},status=status.HTTP_200_OK)
        
        return Response({"status": False, "message": "Order not found", "data": {}},status=status.HTTP_404_NOT_FOUND)
      
      except Exception as e:
          logger.error(f"Order Listing API : {e}")
          return Response({"status": False, "message": "Something went wrong", "data": {}},status=status.HTTP_500_INTERNAL_SERVER_ERROR)