from django.urls import path, include
from core_storage import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"purchase", views.PurchaseViewSet, basename="purchase")
router.register(r"catalog", views.CatalogViewSet, basename="catalog")
router.register(r"arrival", views.InStockViewSet, basename="arrival")

urlpatterns = [
    # path('pin-result/', views.PinMaterial.as_view()),
    path('', include(router.urls))
]
