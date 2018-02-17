from django.urls import path
from gallery_backend import views


urlpatterns = [
    path('backend/', views.ProductCreate.as_view(), name="backend-create"),
    path('backend/list', views.ProductList.as_view(), name="backend-list"),
]
