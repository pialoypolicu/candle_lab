from django.urls import path
from core_storage import views

urlpatterns = [
    path("catalog/", views.GetCatalog.as_view()),
    path('add-product/', views.CreatePurchase.as_view()),
    path('pin-result/', views.PinMaterial.as_view()),
    path('arrival-instock/', views.ArrivalMaterial.as_view())
]
