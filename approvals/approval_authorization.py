from .models import Approvee, ProcurementPlanApprovee, RequisitionFormApprovee, QuoteApprovee


class ApprovalAuthorization:
    def __init__(self, form_type, form_id, user_id, quote_file_id=None):
        self.form_type = form_type
        self.form_id = form_id
        self.user_id = user_id
        self.quote_file_id = quote_file_id
        self.MAXIMUM_ALLOWED_PROCUREMENT_APPROVEES = 3
        self.MAXIMUM_ALLOWED_REQUISITION_APPROVEES = 2
        self.MAXIMUM_ALLOWED_QUOTE_APPROVEES = 4

    def approve_count_limit(self):
        if self.form_type == 'procurement_plan':
            return ProcurementPlanApprovee.objects.filter(procurement_plan__id=self.form_id,
                                                          approvee__name=self.user_id).exists()
        elif self.form_type == 'requisition':
            return RequisitionFormApprovee.objects.filter(requisition__id=self.form_id,
                                                          approvee__name=self.user_id).exists()
        elif self.form_type == "quote":
            return QuoteApprovee.objects.filter(quote__id=self.form_id,
                                                approvee__name=self.user_id, quote_file__id=self.quote_file_id).exists()

    def form_approvals_count(self):
        if self.form_type == 'procurement_plan':
            approval_count = ProcurementPlanApprovee.objects.filter(procurement_plan=self.form_id).count()
            if approval_count > self.MAXIMUM_ALLOWED_PROCUREMENT_APPROVEES:
                return True
            return False
        elif self.form_type == 'requisition':
            approval_count = RequisitionFormApprovee.objects.filter(requisition=self.form_id).count()
            if approval_count > self.MAXIMUM_ALLOWED_REQUISITION_APPROVEES:
                return True
            return False
        elif self.form_type == "quote":
            approval_count = QuoteApprovee.objects.filter(quote_file__id=self.quote_file_id).count()
            if approval_count > self.MAXIMUM_ALLOWED_QUOTE_APPROVEES:
                return True
            return False
