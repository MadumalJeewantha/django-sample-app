from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ShoppingCartItemViewSet

router = DefaultRouter()
router.register(r'cartitems', ShoppingCartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
