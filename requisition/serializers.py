from rest_framework import serializers
from requisition.models import RequisitionForm, Quote, LocalPurchaseOrder, QuoteFile
from authentication.models import User
from supplier.models import Supplier
from department.models import Department


class RequisitionFormSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(slug_field='last_name', queryset=User.objects.all(), required=False)
    supplier = serializers.SlugRelatedField(slug_field='supplier_name', queryset=Supplier.objects.all())
    department = serializers.SlugRelatedField(slug_field='department_name', queryset=Department.objects.all())

    class Meta:
        model = RequisitionForm
        fields = ['id', 'requisition_type', 'req_condition', 'item_type', 'goods_description', 'service_description',
                  'category',
                  'status', 'reason', 'item_name',
                  'quantity', 'unit_cost', 'amount', 'department', 'supplier', 'created_at', 'created_by']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['supplier_name']


class QuoteFileSerializer(serializers.ModelSerializer):
    supplier = serializers.SerializerMethodField()

    class Meta:
        model = QuoteFile
        fields = ['id', 'status', 'supplier', 'quote_file', 'created_at']

    def get_supplier(self, obj):
        return str(obj.supplier.supplier_name)


class LocalPurchaseOrderSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier', required=False)
    address = serializers.SerializerMethodField()
    quote = serializers.CharField(required=False)
    created_by = serializers.SlugRelatedField(slug_field='last_name', queryset=User.objects.all(), required=False)
    order_by = serializers.SlugRelatedField(slug_field='last_name', queryset=User.objects.all(), required=False)

    class Meta:
        model = LocalPurchaseOrder
        fields = ['id', 'supplier_name', 'address', 'quote', 'description_of_goods', 'quantity', 'unit_cost', 'total',
                  'order_by', 'created_by', 'delivery_location', 'delivery_date']

    def get_address(self, obj):
        return str(obj.supplier.address)
