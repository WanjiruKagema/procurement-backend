from rest_framework import serializers
from approvals.models import Approvee, QuoteApprovee
from authentication.models import User


# class StatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Status
#         fields = ['id', 'pending', 'rejected', 'approved']


class ApproveeSerializer(serializers.ModelSerializer):
    approvee_name = serializers.SlugRelatedField(slug_field='first_name', queryset=User.objects.all())
    weight = serializers.IntegerField(required=False)
    approval_status = serializers.CharField(required=True)

    class Meta:
        model = Approvee
        fields = ['id', 'approvee_name', 'weight', 'approval_status', 'requisition', 'procurement_plan', 'comment',
                  'created_at']


class QuoteApproveeSerializer(serializers.ModelSerializer):
    approvee_name = serializers.SlugRelatedField(slug_field='first_name', queryset=User.objects.all())
    weight = serializers.IntegerField(required=False)
    approval_status = serializers.CharField(required=True)

    class Meta:
        model = QuoteApprovee
        fields = ['id', 'approvee', 'quote']


# class QuoteApprovalsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = QuoteApprovals
#         fields = ['id', 'status', 'approvee']


# class ProcurementPlanApprovalsSerializer(serializers.ModelSerializer):
#     # status = serializers.SerializerMethodField()
#     class Meta:
#         model = ProcurementPlanApprovals
#         fields = ['id', 'status', 'procurement_plan', 'approved_at']
#         depth = 1
        #
        # def get_status(self, ProcurementPlanApprovals):
        #     return ProcurementPlanApprovals.status.status
