from builtins import min

from django.db import models
from department.models import Department
from supplier.models import Supplier
from authentication.models import User
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
from safedelete.managers import SafeDeleteManager

TYPE_OF_PURCHASE = [
    ("SGS", "SINGLE SOURCE"),
    ("NML", "NORMAL")
]

ITEM_TYPE = [
    ("GDS", "GOODS"),
    ("SVR", "SERVICE"),
]

YEAR_QUARTER = [
    ("Q1", "Quarter 1"),
    ("Q2", "Quarter 2"),
    ("Q3", "Quarter 3"),
    ("Q4", "Quarter 4"),
]

APPROVAL_STATUS = [
    ('Approved', 'APPROVED'),
    ('Rejected', 'REJECTED'),
    ('Pending', 'PENDING'),
]

CATEGORIES = [
    ("Electronics", "ELECTRONICS"),
    ("Cutlery", "CUTLERY"),
    ("Stationery", "STATIONERY"),
]


# Create your models here.
class ProcurementPlan(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    item_type = models.CharField(choices=ITEM_TYPE, max_length=35)
    good_details = models.CharField(max_length=650, blank=True, default='')
    service_details = models.CharField(max_length=650, blank=True, default='')
    quantity = models.DecimalField(max_digits=12, decimal_places=1)
    category = models.CharField(max_length=35, choices=CATEGORIES, default='', null=True)
    type_of_purchase = models.CharField(choices=TYPE_OF_PURCHASE, max_length=35)
    status = models.CharField(choices=APPROVAL_STATUS, max_length=35, default='Pending')
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default='')
    supplier = models.ForeignKey(Supplier, null=True, on_delete=models.SET_NULL, related_name="+")
    quarter_year = models.CharField(choices=YEAR_QUARTER, max_length=35, default='')
    description = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    objects = SafeDeleteManager()

    # def __unicode__(self):
    #     return  u'%s %s %s' % (self.receiptno, self.type, self.memberno)
