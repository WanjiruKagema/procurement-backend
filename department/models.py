import datetime
import time

from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE, SOFT_DELETE
from safedelete.managers import SafeDeleteManager

DEPARTMENT_NAMES = [
    ("FID", "FINANCE DEPT"),
    ("ITD", "IT DEPT"),
    ("MKD", "Marketing Dept"),
    ("CRD", "Credit Dept"),
    ("CCD", "Customer Care Dept"),
    ("HRD", "Human Capitol Dept")

]


# Create your models here.
class Department(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    department_name = models.CharField(choices=DEPARTMENT_NAMES, max_length=35, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SafeDeleteManager()

    def __str__(self):
        return self.department_name
