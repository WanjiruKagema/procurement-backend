from django.contrib import admin
from .models import Approvee, QuoteApprovee, ProcurementPlanApprovee, RequisitionFormApprovee

# Register your models here.
admin.site.register(Approvee)
# admin.site.register(Status)
admin.site.register(RequisitionFormApprovee)
admin.site.register(QuoteApprovee)
admin.site.register(ProcurementPlanApprovee)
