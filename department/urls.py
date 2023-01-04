from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from department import views

urlpatterns = [
    path('departments/', views.DepartmentList.as_view()),
    path('departments/<int:pk>', views.DepartmentDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)