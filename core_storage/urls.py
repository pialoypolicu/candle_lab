from django.urls import path, include
from core_storage import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"purchase", views.PurchaseViewSet, basename="purchase")
router.register(r"catalog", views.CatalogViewSet, basename="catalog")
router.register(r"arrival", views.ArrivalViewSet, basename="arrival")
router.register(r"instock", views.InStockViewSet, basename="instock")

urlpatterns = [
    path('', include(router.urls)),
]
