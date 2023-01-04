from django.db import models
from authentication.models import User
from requisition.models import RequisitionForm, Quote, QuoteFile
from annual_procurement_plan.models import ProcurementPlan

APPROVAL_STATUS = [
    ('Approved', 'APPROVED'),
    ('Rejected', 'REJECTED'),
    ('Pending', 'PENDING'),
]


# Create your models here.
# class Status(models.Model):
#     pending = models.BooleanField(default=False)
#     rejected = models.BooleanField(default=False)
#     approved = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     objects = models.Manager()


class Approvee(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.IntegerField(blank=True, null=True)
    # requisition = models.ForeignKey(RequisitionForm, on_delete=models.SET_NULL, null=True)
    approval_status = models.BooleanField(default=False)
    comment = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()


class QuoteApproveeManager(models.Manager):
    def create_quote_approvee(self, approvee, quote, quote_file):
        print("Quote Approvee created")
        quote_object = Quote.objects.get(pk=quote)
        quote_file_object = QuoteFile.objects.get(pk=quote_file)
        quote_approvee = self.model(approvee=approvee, quote=quote_object, quote_file=quote_file_object)
        quote_approvee.save()


class QuoteApprovee(models.Model):
    approvee = models.ForeignKey(Approvee, on_delete=models.CASCADE)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    quote_file = models.ForeignKey(QuoteFile, on_delete=models.SET_NULL, null=True)
    approved_at = models.DateTimeField(auto_now_add=True)

    objects = QuoteApproveeManager()


class ProcurementPlanApprovee(models.Model):
    approvee = models.ForeignKey(Approvee, on_delete=models.CASCADE)
    procurement_plan = models.ForeignKey(ProcurementPlan, on_delete=models.CASCADE)
    approved_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()


class RequisitionFormApprovee(models.Model):
    approvee = models.ForeignKey(Approvee, on_delete=models.CASCADE)
    requisition = models.ForeignKey(RequisitionForm, on_delete=models.CASCADE)
    approved_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
