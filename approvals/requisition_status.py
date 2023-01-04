from .models import Approvee


class RequisitionFormStatus:
    def __init__(self, req_id):
        self.requisition_form = None
        self.req_id = req_id
        self.requisition_form_status = None
        self.requisition_form_approve_weights = []
        self.CEO_FINAL_WEIGHT = 40
        self.approval_weights = []
        self.rejection_weights = []
        self.allowed_status = {
            'approved': 'Approved',
            'pending': 'Pending',
            'rejected': 'Rejected'
        }

    def get_all_approvee_weights(self):
        approvee_weights = Approvee.objects.filter(requisitionformapprovee__requisition=self.req_id).values('weight')
        for val in approvee_weights.iterator():
            self.requisition_form_approve_weights.append(val['weight'])
        return self.requisition_form_approve_weights

    def determine_requisition_status(self):
        self.get_all_approvee_weights()

        for weight in self.requisition_form_approve_weights:
            if weight > 0:
                print('------------------------')
                print('append approval weights')
                self.approval_weights.append(weight)
            else:
                print('------------------------')
                print('append rejection weights')
                self.rejection_weights.append(abs(weight))

        # if self.CEO_FINAL_WEIGHT in self.approval_weights:
        #     self.requisition_form_status = self.allowed_status.get('approved')
        #     return
        # if self.CEO_FINAL_WEIGHT in self.rejection_weights:
        #     self.requisition_form_status = self.allowed_status.get('rejected')
        #     return
        # if len(self.approval_weights) == 0 or len(self.rejection_weights) == 1:
        #     print('if Approval Weight isEqual to 1 and Rejection Weight isEqual to 1 set Pending')
        #     self.requisition_form_status = self.allowed_status.get('pending')
        #     return
        # if len(self.approval_weights) == 1 or len(self.rejection_weights) == 0:
        #     print('if Approval Weight isEqual to 1 and Rejection Weight isEqual to 1 set Pending')
        #     self.requisition_form_status = self.allowed_status.get('pending')
        #     return
        # if len(self.approval_weights) == 0 and len(self.rejection_weights) > 1:
        #     self.requisition_form_status = self.allowed_status.get('rejected')
        #     return
        # if len(self.rejection_weights) == 0 and len(self.approval_weights) > 1:
        #     self.requisition_form_status = self.allowed_status.get('approved')
        #     return

        # if len(self.rejection_weights) == 1 and len(self.approval_weights) == 1:
        #     self.requisition_form_status = self.allowed_status.get('pending')
        #     return

        if sum(self.approval_weights) == sum(self.rejection_weights):
            print('---------------------------')
            print('set status to pending if there is equal numbers of approval and rejection weights')
            self.requisition_form_status = self.allowed_status.get('pending')
            return

        if sum(self.approval_weights) > sum(self.rejection_weights):
            print('------------------------')
            print('set status for approval')
            self.requisition_form_status = self.allowed_status.get('approved')
            return
        else:
            print('------------------------')
            print('set status for rejection')
            self.requisition_form_status = self.allowed_status.get('rejected')
            return

    def get_requisition_status(self):
        self.determine_requisition_status()

        print(self.requisition_form_status)
        return self.requisition_form_status
