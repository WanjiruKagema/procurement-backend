from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from supplier import views

urlpatterns = [
    path('suppliers/', views.SupplierList.as_view()),
    path('suppliers/<int:pk>', views.SupplierDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
