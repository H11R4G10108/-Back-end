from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views
router = DefaultRouter()
from rest_framework_simplejwt.views import TokenRefreshView

router.register(r'product', api_views.ProductViewSet)
router.register(r'users', api_views.UserViewSet)
router.register(r'address', api_views.AddressViewSet)
router.register(r'order', api_views.OrderViewSet)
router.register(r'orderdetail', api_views.OrderDetailViewSet)
router.register(r'orderview', api_views.OrderViewReadSet,"orderview")
router.register(r'categoryview', api_views.CategoryProductViewSet,"categoryview")

urlpatterns = [
    path('api/', include((router.urls, 'api'))),
    path('api/token/', api_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', api_views.RegisterView.as_view(), name='auth_register'),
    path('api/change-password/', api_views.ChangePasswordView.as_view(), name='change_password'),
    path('api/user/<int:pk>/address', api_views.AddressList.as_view(), name='address_list'),
    path('api/mark_default_address/<int:pk>/', api_views.mark_default_address, name='mark_default_address'),
    path('api/create-address/', api_views.address_create, name='address_create'),
    path('api/order/<int:pk>/detail', api_views.OrderDetailList.as_view(), name='order_detail_list'),
    path('api/cancel-order/<int:pk>/', api_views.cancel_order, name='cancel_order'),
    path('', api_views.getRoutes),
]
