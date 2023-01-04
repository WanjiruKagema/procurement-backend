from .models import Approvee, ProcurementPlanApprovee
from annual_procurement_plan.models import ProcurementPlan
from django.template.loader import render_to_string
from .mailer.overall_form_status_mail import Mailer


class ProcurementPlanStatus:
    def __init__(self, proc_plan_id):
        self.procurement_plan = None
        self.proc_plan_id = proc_plan_id
        self.procurement_plan_approvee_weights = []
        self.procurement_plan_status = None
        self.CEO_FINAL_WEIGHT = 40
        self.approval_weights = []
        self.rejection_weights = []
        self.context = []
        self.allowed_status = {
            'approved': 'Approved',
            'pending': 'Pending',
            'rejected': 'Rejected'
        }

    def get_all_approvee_weights(self):
        self.approval_weights = []
        self.rejection_weights = []
        self.procurement_plan_approvee_weights = []
        self.procurement_plan = ProcurementPlan.objects.get(pk=self.proc_plan_id)
        procurement_approvees = ProcurementPlanApprovee.objects.filter(procurement_plan=self.proc_plan_id)
        for procurement_approvee in procurement_approvees:
            self.procurement_plan_approvee_weights.append(procurement_approvee.approvee.weight)

        return self.procurement_plan_approvee_weights

    def determine_procurementplan_status(self):
        self.get_all_approvee_weights()

        if len(self.procurement_plan_approvee_weights) < 3:
            self.procurement_plan_status = self.allowed_status.get('pending')
            return
        for weight in self.procurement_plan_approvee_weights:
            if weight > 0:
                print('------------------------')
                print('append approval weights')
                self.approval_weights.append(weight)
            else:
                print('------------------------')
                print('append rejection weights')
                self.rejection_weights.append(abs(weight))

        if len(self.approval_weights) == 0 and len(self.rejection_weights) == 1:
            print('if Approval Weight isEqual to 1 and Rejection Weight isEqual to 1 set Pending')
            self.procurement_plan_status = self.allowed_status.get('pending')
            return
        if len(self.approval_weights) == 1 and len(self.rejection_weights) == 0:
            print('if Approval Weight isEqual to 1 and Rejection Weight isEqual to 1 set Pending')
            self.procurement_plan_status = self.allowed_status.get('pending')
            return

        if len(self.rejection_weights) == 1 and len(self.approval_weights) == 1:
            self.procurement_plan_status = self.allowed_status.get('pending')
            return

        if sum(self.approval_weights) == sum(self.rejection_weights):
            print('---------------------------')
            print('set status to pending if there is equal numbers of approval and rejection weights')
            self.procurement_plan_status = self.allowed_status.get('pending')
            return

        if sum(self.approval_weights) > sum(self.rejection_weights):
            print("sum apr", sum(self.approval_weights))
            print("sum rej", sum(self.rejection_weights))
            print('------------------------')
            print('set status for approval')
            self.procurement_plan_status = self.allowed_status.get('approved')
            return
        else:
            print("sum apr", sum(self.approval_weights))
            print("sum rej", sum(self.rejection_weights))
            print('------------------------')
            print('set status for rejection')
            self.procurement_plan_status = self.allowed_status.get('rejected')
            return

    def send_overall_status_mail(self):
        self.determine_procurementplan_status()

        if self.procurement_plan_status == 'Approved' or self.procurement_plan_status == 'Rejected':
            try:
                subject = 'Final Procurement Plan Status'
                procurement_approvees = ProcurementPlanApprovee.objects.filter(procurement_plan=self.proc_plan_id)
                for procurement_approvee in procurement_approvees:

                    self.context.append({"email": procurement_approvee.approvee.name.email,
                                         "name": procurement_approvee.approvee.name.first_name
                                        })
                self.context.append({
                    "email": self.procurement_plan.created_by.email,
                    "name": self.procurement_plan.created_by.first_name
                })
                mailer = Mailer()
                mailer.send_messages(subject=subject, context=self.context,
                                     form_description=self.procurement_plan.description,
                                     form_status=self.procurement_plan_status)
            except:
                pass

    def get_procurementplan_status(self):
        self.send_overall_status_mail()

        return self.procurement_plan_status
