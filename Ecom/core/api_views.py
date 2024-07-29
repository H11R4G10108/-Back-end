from django.http import JsonResponse
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import UpdateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Product, User, CustomerAddress, Order, OrderDetail, Category
from .serializers import ProductSerializer, UserSerializer, MyTokenObtainPairSerializer, RegisterSerializer, \
    AddressSerializer, OrderSerializer, OrderDetailSerializer, OrderDetailReadSerializer, OrderReadSerializer, \
    ChangePasswordSerializer
from rest_framework import filters
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

class AddressViewSet(viewsets.ModelViewSet):
    queryset = CustomerAddress.objects.all()
    serializer_class = AddressSerializer
    pagination_class = LimitOffsetPagination

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = LimitOffsetPagination

class OrderViewReadSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderReadSerializer
    pagination_class = LimitOffsetPagination
class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    pagination_class = LimitOffsetPagination


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
    '/api/token/',
    '/api/register/',
    '/api/token/refresh/',
        'api/product',
        'api/address',
        'api/users',
        'api/order',
        'api/orderdetail',
        'api/user/<int:pk>/address',
        'api/mark_default_address/<int:pk>/',
        'api/create-address/',
        'api/order/<int:pk>/detail'
        'api/cancel-order/<int:pk>/'
]
    return Response(routes)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class AddressList(generics.ListAPIView):
    queryset = CustomerAddress.objects.all()
    serializer_class = AddressSerializer
    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.kwargs['pk']
        qs = qs.filter(user__id=user_id)
        return qs


@csrf_exempt
def mark_default_address(request, pk):
    if request.method == "POST":
        addressID = request.POST.get('addressID')
        CustomerAddress.objects.update(default=False)
        res = CustomerAddress.objects.filter(pk=addressID).update(default=True)
        msg = {
            'bool': False
        }
        if res:
            msg = {
                'bool': True
            }
    return JsonResponse(msg)

@api_view(['POST'])
def address_create(request):
    default_value = request.POST.get('default')
    if default_value == "true":
        CustomerAddress.objects.update(default=False)
    address_serializer = AddressSerializer(data=request.data)
    if address_serializer.is_valid():
        address_serializer.save()
    return JsonResponse(address_serializer.data, status=status.HTTP_201_CREATED)

class OrderDetailList(generics.ListAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailReadSerializer
    def get_queryset(self):
        qs = super().get_queryset()
        order_id = self.kwargs['pk']
        qs = qs.filter(order__orderID=order_id)
        return qs

@csrf_exempt
def cancel_order(request, pk):
    if request.method == "POST":
        order_id = request.POST.get('orderID')
        res = Order.objects.filter(pk=order_id).update(status=5)
        msg = {
            'bool': False
        }
        if res:
            msg = {
                'bool': True
            }
    return JsonResponse(msg)

class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryProductViewSet(viewsets.ReadOnlyModelViewSet):
    search_fields = ['category__category']
    filter_backends = (filters.SearchFilter,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderReadSerializer
    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.kwargs['pk']
        qs = qs.filter(user__id=user_id)
        return qs
