from requisition.models import Quote, QuoteFile
from requisition.models import LocalPurchaseOrder


class GenerateLPO:
    def __init__(self, quote_file_id, user_instance):
        self.quote_file_id = quote_file_id
        self.quote_file_status = None
        self.quote_file_obj = None
        self.user_instance = user_instance
        self.quote_id = None
        self.quote_obj = None

    def get_quote_file(self):
        quote_file_instance = QuoteFile.objects.get(pk=self.quote_file_id)
        self.quote_file_obj = quote_file_instance
        self.quote_file_status = quote_file_instance.status
        self.quote_id = quote_file_instance.quote.id

    def get_quote(self):
        self.get_quote_file()

        quote_instance = Quote.objects.get(pk=self.quote_id)
        self.quote_obj = quote_instance
        self.quote_file_status = self.quote_file_obj.status

    def create_delete_local_purchase_order(self):
        self.get_quote()

        print(self.quote_file_status)
        if self.quote_file_status == 'Approved':
            print('Create an LPO if Quote Approval Status == Approved')
            lpo_instance = LocalPurchaseOrder()
            lpo_instance.quote = self.quote_obj
            lpo_instance.supplier = self.quote_file_obj.supplier
            lpo_instance.quantity = self.quote_obj.requisition.quantity
            lpo_instance.unit_cost = self.quote_obj.requisition.unit_cost
            lpo_instance.total = self.quote_obj.requisition.amount
            lpo_instance.description_of_goods = self.quote_obj.requisition.goods_description
            lpo_instance.order_by = self.quote_obj.requisition.created_by
            lpo_instance.created_by = self.user_instance
            lpo_instance.save()

        elif self.quote_file_status == 'Rejected':
            if LocalPurchaseOrder.objects.filter(quote=self.quote_id).exists():
                lpo_instance = LocalPurchaseOrder.objects.get(quote=self.quote_id)
                lpo_instance.delete()

