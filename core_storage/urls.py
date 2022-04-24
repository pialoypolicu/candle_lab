from django.urls import path
from core_storage import views

urlpatterns = [
    path('add-product/', views.APICat.as_view())
]
