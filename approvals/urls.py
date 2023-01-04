from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from approvals import views

urlpatterns = [
    path('approvee/', views.ApproveeList.as_view()),
    path('approvee/<int:pk>', views.ApproveeDetail.as_view()),
    path('proc/approvee/<int:pk>/', views.ProcurementPlanApproveeList.as_view()),
    path('quote/approvee/', views.QuoteApproveeList.as_view()),
    path('requisition/approvee/<int:pk>', views.RequisitionFormApproveeList.as_view()),
    path('proc/approvee/status/<int:procurementplan>', views.ProcurementPlanApproveeView.as_view()),
    path('req/approvee/status/<int:requisition>', views.RequisitionFormApproveeView.as_view()),
    path('quote/approvee/status/<int:quote_id>/<int:quote_file_id>', views.QuoteApproveeView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)

