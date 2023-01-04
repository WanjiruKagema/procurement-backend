from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from annual_procurement_plan import views

urlpatterns = [
    path('proc-plan/', views.ProcurementPlanList.as_view()),
    path('proc-plan/<int:pk>', views.ProcurementPlanDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
