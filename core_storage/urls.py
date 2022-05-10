from django.urls import path, include
from core_storage import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"purchase", views.PurchaseViewSet)

urlpatterns = [
    path("catalog/", views.catalog_view, name="get_catalog"),
    path('pin-result/', views.PinMaterial.as_view()),
    path('arrival-instock/', views.ArrivalMaterial.as_view()),
    path('', include(router.urls))
]
