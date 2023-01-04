from django.contrib import admin
from .models import RequisitionForm, Quote, QuoteFile, LocalPurchaseOrder

# Register your models here.
admin.site.register(RequisitionForm)
admin.site.register(Quote)
admin.site.register(QuoteFile)
admin.site.register(LocalPurchaseOrder)

