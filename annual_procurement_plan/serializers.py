from rest_framework import serializers
from annual_procurement_plan.models import ProcurementPlan
from department.models import Department
from supplier.models import Supplier
from authentication.models import User


class ProcurementPlanSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(slug_field='first_name', queryset=User.objects.all(), required=False)
    supplier = serializers.SlugRelatedField(slug_field='supplier_name', queryset=Supplier.objects.all())
    department = serializers.SlugRelatedField(slug_field='department_name', queryset=Department.objects.all())
    status = serializers.CharField(required=False)

    class Meta:
        model = ProcurementPlan
        fields = ['id', 'item_type', 'good_details', 'service_details', 'status', 'quantity', 'type_of_purchase',
                  'budget', 'category', 'description', 'department', 'supplier', 'quarter_year', 'created_at', 'created_by']

