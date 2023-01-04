from django.shortcuts import render
from .models import RequisitionForm, Quote, LocalPurchaseOrder
from supplier.models import Supplier
from .serializers import LocalPurchaseOrderSerializer, RequisitionFormSerializer, QuoteFileSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import QuoteFile


# Create your views here.
# Requisition Form Views
class RequisitionFormList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):

        if request.user.is_head_department or request.user.is_staff:
            req_form = RequisitionForm.objects.filter(department=request.user.department).order_by('id')
            serializer = RequisitionFormSerializer(req_form, many=True)
            return Response(serializer.data)
        elif request.user.is_procurement_officer or request.user.is_ceo or request.user.is_procurement_officer:
            req_form = RequisitionForm.objects.all().order_by('id')
            serializer = RequisitionFormSerializer(req_form, many=True)
            return Response(serializer.data)
        elif request.user.is_staff:
            req_form = RequisitionForm.objects.filter(department=request.user.department).order_by('id')
            serializer = RequisitionFormSerializer(req_form, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        print(request.user)
        serializer = RequisitionFormSerializer(data=request.data)
        if serializer.is_valid():
            requisition_instance = serializer.save()
            requisition_instance.department = request.user.department
            requisition_instance.created_by = request.user
            requisition_instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequisitionFormDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return RequisitionForm.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk):
        req_form = self.get_object(pk)
        serializer = RequisitionFormSerializer(req_form)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        req_form = self.get_object(pk)
        serializer = RequisitionFormSerializer(req_form, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        req_form = self.get_object(pk)
        req_form.delete()
        # req_forms = RequisitionForm.objects.get_queryset()
        # serializer = RequisitionFormSerializer(req_forms, many=True)
        return Response({"message": "Req Deleted Successfully", "status": status.HTTP_200_OK},
                        status=status.HTTP_100_CONTINUE)


class ApprovedRequisition(APIView):
    # Get all Approved Requisition
    def get(self, request, format=None):
        req_form = RequisitionForm.objects.filter(status='Approved')
        serializer = RequisitionFormSerializer(req_form, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Create your views here.
# Quote Views
class QuoteList(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, requisition, format=None):
        requisition = requisition
        data = request.data.dict()
        if not requisition:
            return Response({'error': "Missing Requisition"}, status=status.HTTP_400_BAD_REQUEST)

        requisition_instance = RequisitionForm.objects.get(pk=requisition)
        if Quote.objects.filter(requisition=requisition).exists():
            quote_instance = Quote.objects.get(requisition=requisition)

            if QuoteFile.objects.filter(quote=quote_instance.id, status='Approved').exists():
                return Response({"message": "Can't Upload, A Quote File Has Already Been Approved",
                                 "status": status.HTTP_204_NO_CONTENT})
            else:
                for key in data:
                    supplier_instance = Supplier.objects.get(pk=int(key))
                    QuoteFile.objects.create(quote_file=data.get(key), quote=quote_instance,
                                             supplier=supplier_instance)

                return Response({"message": "Quote File has been updated successfully", "status": status.HTTP_200_OK})
        else:
            quote_instance = Quote(requisition=requisition_instance, created_by=request.user)
            quote_instance.save()
            for key in data:
                supplier_instance = Supplier.objects.get(pk=int(key))
                QuoteFile.objects.create(quote_file=data.get(key), quote=quote_instance,
                                         supplier=supplier_instance)

            return Response({"message": "Quote has been uploaded successfully", "status": status.HTTP_200_OK})


class QuoteDetailForRequisition(APIView):
    def get(self, request, pk, format=None):
        try:
            quote = Quote.objects.get(requisition=pk)
        except:
            return Response({
                "status": status.HTTP_204_NO_CONTENT,
                "message": "No uploaded quotes for requisition"
            })
        if QuoteFile.objects.filter(quote=quote.id).exists():
            quote_files = QuoteFile.objects.filter(quote=quote.id).order_by('id')
            serialized_quotes = QuoteFileSerializer(quote_files, many=True).data

            return Response({
                "status": status.HTTP_200_OK,
                "quote": quote.id,
                "quote_files": serialized_quotes
            })
        return Response({
            "status": status.HTTP_204_NO_CONTENT,
            "message": "No Quote Files For The Quote"
        })


class QuoteFileDetail(APIView):
    def delete(self, request, pk, format=None):
        quote_file = QuoteFile.objects.get(pk=pk)
        quote_file.delete()
        return Response({"message": "Quote File Deleted"}, status=status.HTTP_100_CONTINUE)

    # def put(self, request, pk, format=None):
    #     quote = self.get_object(pk)
    #     serializer = QuoteSerializer(quote, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk, format=None):
    #     quote = self.get_object(pk)
    #     quote.quote_file.delete()
    #     quote.delete()
    #     quotes = Quote.objects.all()
    #     serializer = QuoteSerializer(quotes, many=True)
    #     return Response(serializer.data, status=status.HTTP_100_CONTINUE)


# Local Purchase Order Views
class LocalPurchaseOrderList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        local_purchase_order = LocalPurchaseOrder.objects.all()
        print(local_purchase_order)
        serializer = LocalPurchaseOrderSerializer(local_purchase_order, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        if 'quote' not in request.data:
            return Response({"error": "missing quote value", "status": status.HTTP_204_NO_CONTENT})
        if 'supplier' not in request.data:
            return Response({"error": "missing supplier value", "status": status.HTTP_204_NO_CONTENT})
        supplier_instance = Supplier.objects.get(pk=data['supplier'])
        quote_instance = Quote.objects.get(pk=data['quote'])

        lpo_instance = LocalPurchaseOrder()
        if 'unit_cost' and 'quantity' and 'total' and 'description_of_goods' 'delivery_location' 'delivery_date' not in data:
            lpo_instance = LocalPurchaseOrder(quote=quote_instance, supplier=supplier_instance, total=data['total'],
                                              quantity=data['quantity'], unit_cost=data['unit_cost'],
                                              created_by=request.user, delivery_location=data['delivery_location'],
                                              delivery_date=data['delivery_date'],
                                              description_of_goods=data['description_of_goods'])
            lpo_instance.save()
            return Response({
                "supplier": lpo_instance.supplier.supplier_name,
                "address": lpo_instance.supplier.address,
                "total": lpo_instance.total,
                "unit_cost": lpo_instance.unit_cost,
                "quantity": lpo_instance.quantity,
                "created_by": lpo_instance.created_by.first_name,
                "order_by": lpo_instance.quote.requisition.created_by.first_name,
                "delivery_date": lpo_instance.delivery_date
            })
        else:
            return Response({"error": "Missing LPO values", "status": status.HTTP_408_REQUEST_TIMEOUT})


class LocalPurchaseOrderDetail(APIView):
    def get_object(self, pk):
        try:
            return LocalPurchaseOrder.objects.get(pk=pk)
        except LocalPurchaseOrder.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        local_purchase_order = self.get_object(pk)
        serializer = LocalPurchaseOrderSerializer(local_purchase_order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        local_purchase_order = self.get_object(pk)
        serializer = LocalPurchaseOrderSerializer(local_purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        local_purchase_order = self.get_object(pk)
        local_purchase_order.delete()
        return Response({"Delete": "Successful"}, status=status.HTTP_204_NO_CONTENT)


# Reports
class RequestReports(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):

        if request.user.is_head_department or request.user.is_staff:
            approved_req_count = RequisitionForm.objects.filter(department=request.user.department,
                                                                status='Approved').count()
            pending_req_count = RequisitionForm.objects.filter(department=request.user.department,
                                                               status='Pending').count()
            rejected_req_count = RequisitionForm.objects.filter(department=request.user.department,
                                                                status='Rejected').count()
        elif request.user.is_procurement_officer or request.user.is_ceo or request.user.is_procurement_officer:
            approved_req_count = RequisitionForm.objects.filter(status='Approved').count()
            pending_req_count = RequisitionForm.objects.filter(status='Pending').count()
            rejected_req_count = RequisitionForm.objects.filter(status='Rejected').count()

        elif request.user.is_staff:
            approved_req_count = RequisitionForm.objects.filter(department=request.user.department,
                                                                status='Approved').count()
            pending_req_count = RequisitionForm.objects.filter(department=request.user.department,
                                                               status='Pending').count()
            rejected_req_count = RequisitionForm.objects.filter(department=request.user.department,
                                                                status='Rejected').count()

        num_of_suppliers = Supplier.objects.count()
        return Response({
            "approved_requests": approved_req_count,
            "pending_requests": pending_req_count,
            "rejected_requests": rejected_req_count,
            "supplier_count": num_of_suppliers,
            "status": status.HTTP_200_OK
        })


class RequisitionReportsDetails(APIView):
    def get(self, request):

        if request.user.is_head_department or request.user.is_staff:
            req_approved = RequisitionForm.objects.filter(department=request.user.department,
                                                          status='Approved').order_by('id')
            req_pending = RequisitionForm.objects.filter(department=request.user.department, status='Pending').order_by(
                'id')
            req_rejected = RequisitionForm.objects.filter(department=request.user.department,
                                                          status='Rejected').order_by('id')
        elif request.user.is_procurement_officer or request.user.is_ceo or request.user.is_procurement_committee:
            req_approved = RequisitionForm.objects.filter(status='Approved').order_by('id')
            req_pending = RequisitionForm.objects.filter(status='Pending').order_by('id')
            req_rejected = RequisitionForm.objects.filter(status='Rejected').order_by('id')
        elif request.user.is_staff:
            req_approved = RequisitionForm.objects.filter(department=request.user.department,
                                                          status='Approved').order_by('id')
            req_pending = RequisitionForm.objects.filter(department=request.user.department, status='Pending').order_by(
                'id')
            req_rejected = RequisitionForm.objects.filter(department=request.user.department,
                                                          status='Rejected').order_by('id')

        req_serialized_approved = RequisitionFormSerializer(req_approved, many=True).data
        req_serialized_pending = RequisitionFormSerializer(req_pending, many=True).data
        req_serialized_rejected = RequisitionFormSerializer(req_rejected, many=True).data

        return Response({
            "status": status.HTTP_200_OK,
            "approved": req_serialized_approved,
            "pending": req_serialized_pending,
            "rejected": req_serialized_rejected
        })
