#emall/orders/views.py
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status, permissions
from rest_framework.pagination import LimitOffsetPagination
from user.rbac import IsAdmin, IsGetOrAdmin
from .models import Orders
from rest_framework.response import Response
from .serializers import OrdersSerializer
# Create your views here.

def index(request):
    return JsonResponse({"message": "Welcome !"})


# List and create new Orders
class OrdersListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Orders.objects.filter(is_deleted=False, status=True).order_by('id')
    serializer_class = OrdersSerializer
    pagination_class = LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        try:
            user = self.request.user
            # access queryset from class level object
            queryset = self.get_queryset()
            if user.user_scope in ("MANAGER", "ADMIN"):
                queryset = queryset # No changes in query set for this condition
            else:
                 # added extra filter for queryset.
                 queryset = queryset.filter({'customer':user})
            
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
            print(e)
            return Response("Something went wrong", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrdersDetailsAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsGetOrAdmin,)
    queryset = Orders.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = OrdersSerializer