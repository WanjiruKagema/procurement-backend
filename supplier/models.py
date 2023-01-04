from django.db import models
from authentication.models import User
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE
from safedelete.managers import SafeDeleteManager

CATEGORIES = [
    ("Electronics", "ELECTRONICS"),
    ("Cutlery", "CUTLERY"),
    ("Stationery", "STATIONERY"),
]


# Create your models here.
class Supplier(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    supplier_name = models.CharField(max_length=35)
    supplier_contact = models.CharField(max_length=65)
    category = models.CharField(max_length=35, choices=CATEGORIES, default='', null=True)
    address = models.CharField(max_length=65)
    description = models.TextField()
    prequalified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    objects = SafeDeleteManager()

    def __str__(self):
        return self.supplier_name
