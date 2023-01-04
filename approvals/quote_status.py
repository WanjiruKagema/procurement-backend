from approvals.models import QuoteApprovee
from approvals.models import Approvee
from requisition.models import QuoteFile, Quote
from .mailer.overall_form_status_mail import Mailer


class QuoteStatus:
    def __init__(self, quote_id, quote_file_id):
        self.quote = None
        self.quote_obj = None
        self.quote_id = quote_id
        self.quote_file_id = quote_file_id
        self.quote_file = None
        self.quote_status = None
        self.context = []
        self.quote_approve_weights = []
        self.CEO_FINAL_WEIGHT = 40
        self.approval_weights = []
        self.rejection_weights = []
        self.allowed_status = {
            'approved': 'Approved',
            'pending': 'Pending',
            'rejected': 'Rejected'
        }

    def check_if_quote_file_already_in_quote_approvals(self):
        if QuoteApprovee.objects.filter(quote_file_id=self.quote_file_id).count() >= 2:
            self.quote_file = QuoteFile.objects.get(pk=self.quote_file_id)
            return True
        else:
            self.quote_file = QuoteFile.objects.get(pk=self.quote_file_id)
            self.quote_file.status = self.allowed_status.get('pending')
            self.quote_file.save()
            return False
        print("Quote File ID", self.quote_file_id)

    def get_all_approvee_weights(self):
        self.check_if_quote_file_already_in_quote_approvals()
        self.approval_weights = []
        self.rejection_weights = []
        self.quote_approve_weights = []
        quote_approvees = QuoteApprovee.objects.filter(quote_file=self.quote_file_id, quote=self.quote_id)
        for quote_approvee in quote_approvees:
            self.quote_approve_weights.append(quote_approvee.approvee.weight)
        return self.quote_approve_weights

    def determine_quote_status(self):
        self.get_all_approvee_weights()

        if (len(self.quote_approve_weights) < 3) and (self.CEO_FINAL_WEIGHT in self.quote_approve_weights):
            self.quote_file.status = self.allowed_status.get('approved')
            self.quote_file.save()
            return

        if (len(self.quote_approve_weights) < 3) and (-abs(self.CEO_FINAL_WEIGHT) in self.quote_approve_weights):
            self.quote_file.status = self.allowed_status.get('rejected')
            self.quote_file.save()
            return

        if len(self.quote_approve_weights) < 3:
            print('if Approval Weight isEqual to 1 and Rejection Weight isEqual to 1 set Pending')
            self.quote_file.status = self.allowed_status.get('pending')
            self.quote_file.save()
            return

        if self.CEO_FINAL_WEIGHT in self.quote_approve_weights:
            self.quote_file.status = self.allowed_status.get('approved')
            self.quote_file.save()
            return
        if -abs(self.CEO_FINAL_WEIGHT) in self.quote_approve_weights:
            self.quote_file.status = self.allowed_status.get('rejected')
            self.quote_file.save()
            return

        for weight in self.quote_approve_weights:
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
            self.quote_file.status = self.allowed_status.get('pending')
            self.quote_file.save()
            return
        if len(self.approval_weights) == 1 and len(self.rejection_weights) == 0:
            print('if Approval Weight isEqual to 1 and Rejection Weight isEqual to 1 set Pending')
            self.quote_file.status = self.allowed_status.get('pending')
            self.quote_file.save()
            return

        if len(self.rejection_weights) == 1 and len(self.approval_weights) == 1:
            self.quote_file.status = self.allowed_status.get('pending')
            self.quote_file.save()
            return

        if sum(self.approval_weights) == sum(self.rejection_weights):
            print('---------------------------')
            print('set status to pending if there is equal numbers of approval and rejection weights')
            self.quote_file.status = self.allowed_status.get('pending')
            self.quote_file.save()
            return

        if sum(self.approval_weights) > sum(self.rejection_weights):
            print("sum apr", sum(self.approval_weights))
            print("sum rej", sum(self.rejection_weights))
            print('------------------------')
            print('set status for approval')
            self.quote_file.status = self.allowed_status.get('approved')
            self.quote_file.save()
            return
        else:
            print('------------------------')
            print('set status for rejection')
            self.quote_file.status = self.allowed_status.get('rejected')
            self.quote_file.save()
            return

    def set_quotes_to_reject_if_quote_status_is_approved(self):
        self.determine_quote_status()

        if self.quote_file.status == 'Approved':
            quote_quote_files = QuoteFile.objects.filter(quote=self.quote_id)
            for quote_file in quote_quote_files:
                if quote_file.status == 'Pending':
                    quote_file.status = 'Rejected'
                    quote_file.save()
        elif self.quote_file.status == 'Pending' or self.quote_file.status == 'Rejected':
            quote_quote_files = QuoteFile.objects.filter(quote=self.quote_id)
            for quote_file in quote_quote_files:
                if quote_file.status == 'Pending':
                    quote_file.status = 'Pending'
                    quote_file.save()

    def send_mail_for_final_quote_file_status(self):
        self.set_quotes_to_reject_if_quote_status_is_approved()
        self.quote_obj = Quote.objects.filter(pk=self.quote_id)
        if self.quote_file.status == 'Approved':
            try:
                subject = 'Final Selected Supplier'
                quote_approvees = QuoteApprovee.objects.filter(quote_file=self.quote_file_id, quote=self.quote_id)
                for quote_approvee in quote_approvees:
                    self.context.append({"email": quote_approvee.approvee.name.email,
                                         "name": quote_approvee.approvee.name.first_name
                                         })
                # mailer = Mailer()
                # mailer.send_messages(subject=subject, context=self.context,
                #                      form_description=self.quote_obj.requisition.item_type,
                #                      supplier=self.quote_file.supplier.supplier_name,
                #                      form_status=self.quote_file.status)
            except:
                pass

    def get_quote_status(self):
        self.send_mail_for_final_quote_file_status()
        return self.quote_file.status
