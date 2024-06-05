from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views
router = DefaultRouter()

router.register(r'product', api_views.ProductViewSet)

urlpatterns = [
    path('api/', include((router.urls, 'api'))),
]
