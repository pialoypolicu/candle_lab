from django.urls import include, path
from rest_framework import routers

from core_storage import views

router = routers.DefaultRouter()
router.register(r"purchase", views.PurchaseViewSet, basename="purchase")
router.register(r"catalog", views.CatalogViewSet, basename="catalog")
router.register(r"arrival", views.ArrivalViewSet, basename="arrival")
router.register(r"instock", views.InStockViewSet, basename="instock")
urlpatterns = [
    path("production/", views.ProductionViewSet.as_view({"patch": "update"})),
    path("", include(router.urls))
]
