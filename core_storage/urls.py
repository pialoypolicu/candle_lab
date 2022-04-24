from django.urls import path
from core_storage import views

urlpatterns = [
    path('add-product/', views.CreatePurchase.as_view()),
    path('pin-result/', views.PinMaterial.as_view()),
    path('arrrival', views.ArrivalMaterial.as_view())
]
