from django.urls import path
from gallery_backend import views


urlpatterns = [
    path('backend/', views.ProductCreate.as_view()),
]