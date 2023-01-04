from django.db import models
from authentication.models import User
from department.models import Department
from supplier.models import Supplier
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE, SOFT_DELETE
from safedelete.managers import SafeDeleteManager

# Create your models here.
REQUISITION_TYPE = [
    ("SGS", "SINGLE SOURCE"),
    ("NML", "NORMAL")
]

ITEM_TYPE = [
    ("GDS", "GOODS"),
    ("SVR", "SERVICE"),
]

APPROVAL_STATUS = [
    ('Approved', 'APPROVED'),
    ('Rejected', 'REJECTED'),
    ('Pending', 'PENDING'),
]

REQ_CONDITION = [
    ('Budgeted', 'BUDGETED'),
    ('Emergency', 'EMERGENCY'),
    ('Unplanned', 'UNPLANNED')
]

CATEGORIES = [
    ("Electronics", "ELECTRONICS"),
    ("Cutlery", "CUTLERY"),
    ("Stationery", "STATIONERY"),
]


class RequisitionForm(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    requisition_type = models.CharField(choices=REQUISITION_TYPE, max_length=35)
    item_type = models.CharField(choices=ITEM_TYPE, max_length=35)
    goods = models.CharField(max_length=60, default='')
    services = models.CharField(max_length=60, default='')
    item_name = models.CharField(max_length=65, default='')
    category = models.CharField(max_length=35, choices=CATEGORIES, default='', null=True)
    goods_description = models.CharField(max_length=60, null=True, blank=True, default='')
    service_description = models.CharField(max_length=60, null=True, blank=True, default='')
    status = models.CharField(choices=APPROVAL_STATUS, max_length=35, default='Pending')
    req_condition = models.CharField(choices=REQ_CONDITION, max_length=35, default='')
    reason = models.TextField(default='')
    quantity = models.DecimalField(max_digits=5, decimal_places=1)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    objects = SafeDeleteManager()


class Quote(models.Model):
    requisition = models.ForeignKey(RequisitionForm, on_delete=models.CASCADE, default='')
    created_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    objects = models.Manager()


class QuoteFile(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    quote_file = models.FileField(upload_to='quotes/%Y/%m/%d/', default='')
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, default='')
    status = models.CharField(choices=APPROVAL_STATUS, max_length=35, default='Pending')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SafeDeleteManager()

    # def delete(self, using=None):
    #     self.quote_file.storage.delete(self.quote_file)
    #     super().delete()


class LocalPurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    description_of_goods = models.CharField(max_length=65, default='')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    order_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="firstName")
    delivery_location = models.CharField(max_length=35, blank=True, null=True)
    delivery_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    objects = models.Manager()
