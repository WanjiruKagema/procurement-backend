from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from requisition import views

urlpatterns = [
    path('requisitions/', views.RequisitionFormList.as_view()),
    path('requisitions/<int:pk>', views.RequisitionFormDetail.as_view()),
    path('requisitions/approved', views.ApprovedRequisition.as_view()),
    path('quotes/<int:requisition>', views.QuoteList.as_view()),
    path('quotes/requisition/<int:pk>', views.QuoteDetailForRequisition.as_view()),
    path('localpurchaseorder/', views.LocalPurchaseOrderList.as_view()),
    path('localpurchaseorder/<int:pk>', views.LocalPurchaseOrderDetail.as_view()),
    path('requisition/reports/', views.RequestReports.as_view()),
    path('dashboard/req/reports', views.RequisitionReportsDetails.as_view()),
    path('quotefile/<int:pk>', views.QuoteFileDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
