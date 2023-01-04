from django.shortcuts import render
from .models import Approvee, QuoteApprovee, ProcurementPlanApprovee, RequisitionFormApprovee
from requisition.models import RequisitionForm, Quote, QuoteFile
from annual_procurement_plan.models import ProcurementPlan
from .serializers import ApproveeSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from approvals.procurement_plan_status import ProcurementPlanStatus
from approvals.approvee_weights import get_weight
from approvals.requisition_status import RequisitionFormStatus
from approvals.approval_authorization import ApprovalAuthorization
from approvals.quote_status import QuoteStatus
from approvals.generate_lpo import GenerateLPO
from .mailer.approvee_emails import procurement_approve_email


# Create your views here.
# Approvee views


class ProcurementPlanApproveeList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk, format=None):
        data = request.data
        print(data)
        procurement_plan = pk
        print("pp", procurement_plan)

        if not procurement_plan:
            print('------------------------------')
            print('procuremnt plan does not exist')
            return Response({"error": "Missing Procurement Plan"}, status=status.HTTP_400_BAD_REQUEST)

        print('-----------------------------------------------------')
        print('check if procurement plan was created by current user')
        procurement_plan_object = ProcurementPlan.objects.get(pk=procurement_plan)
        if procurement_plan_object.created_by == request.user:
            return Response({"error": "You cannot approve/reject a Procurement Plan you created"},
                            status=status.HTTP_400_BAD_REQUEST)

        print('-------------------------')
        print('Check if the Approvee is authorized to make an approval')
        authorization_instance = ApprovalAuthorization('procurement_plan', procurement_plan, request.user.id)

        if authorization_instance.approve_count_limit():
            return Response({"error": "Approvee already made an approval status"}, status=status.HTTP_400_BAD_REQUEST)
        if authorization_instance.form_approvals_count():
            return Response({"error": "Allowed number of Approvals exceeded"}, status=status.HTTP_400_BAD_REQUEST)

        print("-------------------------")
        print("Create an Approvee Object")

        approvee_object = Approvee()
        approvee_object.name = request.user
        approvee_object.approval_status = data['approval_status']

        if 'comment' in data:
            approvee_object.comment = data['comment']

        print("--------------------------------------------------")
        print("Assign Approvee Weights based on their permissions")
        if request.user.is_head_department:
            if data['approval_status']:
                approvee_object.weight = get_weight('is_head_department')
            else:
                print(-abs(int(get_weight('is_head_department'))))
                approvee_object.weight = -abs(int(get_weight('is_head_department')))

        if request.user.is_procurement_committee:
            if data['approval_status']:
                approvee_object.weight = get_weight('is_procurement_committee')
            else:
                approvee_object.weight = -abs(int(get_weight('is_procurement_committee')))

        if request.user.is_procurement_officer:
            if data['approval_status']:
                approvee_object.weight = get_weight('is_procurement_officer')
            else:
                approvee_object.weight = -abs(int(get_weight('is_procurement_officer')))

        if request.user.is_head_of_finance:
            if data['approval_status']:
                approvee_object.weight = get_weight('is_head_finance')
            else:
                approvee_object.weight = -abs(int(get_weight('is_head_finance')))

        if request.user.is_ceo:
            if data['approval_status']:
                approvee_object.weight = get_weight('is_ceo')
            else:
                approvee_object.weight = -abs(int(get_weight('is_ceo')))
        approvee_object.save()

        print("----------------------------------")
        print("Create A Procurement Plan Instance")
        prcurement_plan_instance = ProcurementPlan.objects.get(pk=procurement_plan)

        print("--------------------------------------")
        print("Create A Procurement Approvee Instance")
        procuremenplan_approvee_instance = ProcurementPlanApprovee()
        procuremenplan_approvee_instance.approvee = approvee_object
        procuremenplan_approvee_instance.procurement_plan = prcurement_plan_instance
        procuremenplan_approvee_instance.save()

        print("---------------------")
        print("Updating ProcurementPlan Status")
        procurement_plan_status = ProcurementPlanStatus(procurement_plan)
        print(procurement_plan_status.get_all_approvee_weights())

        print("--------------------------------")
        print("Create A ProcurementPlan Approvee Instance")

        print("------------------------------------")
        print("update status of the ProcurementPlan")
        procurement_plan = ProcurementPlan.objects.get(pk=procurement_plan)
        procurement_plan.status = procurement_plan_status.get_procurementplan_status()
        procurement_plan.save()
        print('send approval recorded email')
        try:
            email = procurement_approve_email(approvee_name=request.user.first_name,
                                              approvee_comment=approvee_object.comment,
                                              approvee_email=request.user.email,
                                              date=procuremenplan_approvee_instance.approved_at,
                                              proc_status='Approved' if data['approval_status'] else 'Rejected',
                                              proc_description=prcurement_plan_instance.description)
            email.send()
        except:
            pass

        return Response({
            "success": "Procurement Plan Status Recorded",
            "status": status.HTTP_200_OK,
            "procurement_plan": {
                "id": procurement_plan.id,
                "status": procurement_plan.status
            }
        })


# class ProcurementPlanApproveeDetail(APIView):
#     def put(self, request, ):


class ProcurementPlanApproveeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # Get The Approval Status of a User
    def get(self, request, procurementplan):
        if ProcurementPlanApprovee.objects.filter(procurement_plan__id=procurementplan,
                                                  approvee__name=request.user.id).exists():
            procurement_plan_approvee = ProcurementPlanApprovee.objects.get(procurement_plan__id=procurementplan,
                                                                            approvee__name=request.user.id)
            return Response({
                "status": status.HTTP_200_OK,
                "approval_status": procurement_plan_approvee.approvee.approval_status,
                "comment": procurement_plan_approvee.approvee.comment,
                "approved_at": procurement_plan_approvee.approvee.created_at
            })

        return Response({
            "status": status.HTTP_204_NO_CONTENT,
            "message": "No Approval Status Recorded"
        })

    # Update Approvee Details and Update Procurement Plan Overall Status
    def put(self, request, procurementplan):
        data = request.data
        print(data)

        if ProcurementPlanApprovee.objects.filter(procurement_plan__id=procurementplan,
                                                  approvee__name=request.user.id).exists():
            procurement_plan_approvee = ProcurementPlanApprovee.objects.get(procurement_plan__id=procurementplan,
                                                                            approvee__name=request.user.id)
            print("true")
            approvee_id = procurement_plan_approvee.approvee.id

            approvee_instance = Approvee.objects.get(pk=approvee_id)
            if 'approval_status' in data:
                approvee_instance.approval_status = data['approval_status']
            if 'comment' in data:
                approvee_instance.comment = data['comment']
            print("--------------------------------------------------")
            print("Assign Approvee Weights based on their permissions")
            if request.user.is_head_department:
                if data['approval_status']:
                    approvee_instance.weight = get_weight('is_head_department')
                else:
                    print(-abs(int(get_weight('is_head_department'))))
                    approvee_instance.weight = -abs(int(get_weight('is_head_department')))

            if request.user.is_procurement_committee:
                if data['approval_status']:
                    approvee_instance.weight = get_weight('is_procurement_committee')
                else:
                    approvee_instance.weight = -abs(int(get_weight('is_procurement_committee')))

            if request.user.is_procurement_officer:
                if data['approval_status']:
                    approvee_instance.weight = get_weight('is_procurement_officer')
                else:
                    approvee_instance.weight = -abs(int(get_weight('is_procurement_officer')))

            if request.user.is_head_of_finance:
                if data['approval_status']:
                    approvee_instance.weight = get_weight('is_head_finance')
                else:
                    approvee_instance.weight = -abs(int(get_weight('is_head_finance')))

            if request.user.is_ceo:
                if data['approval_status']:
                    approvee_instance.weight = get_weight('is_ceo')
                else:
                    approvee_instance.weight = -abs(int(get_weight('is_ceo')))

            approvee_instance.save()
            print(approvee_instance.weight)
            print("---------------------")
            print("Updating ProcurementPlan Status")
            procurement_plan_status = ProcurementPlanStatus(procurementplan)
            print(procurement_plan_status.get_all_approvee_weights())

            print("--------------------------------")
            print("Create A ProcurementPlan Approvee Instance")

            print("------------------------------------")
            print("update status of the ProcurementPlan")
            procurement_plan = ProcurementPlan.objects.get(pk=procurementplan)
            procurement_plan.status = procurement_plan_status.get_procurementplan_status()
            procurement_plan.save()

            return Response({
                "status": status.HTTP_200_OK,
                "approval_status": approvee_instance.approval_status,
                "comment": approvee_instance.comment
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "No record Found"
        })


class RequisitionFormApproveeList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk, format=None):
        data = request.data
        requisition = pk

        if not requisition:
            return Response({"error": "Missing Requisition"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        print('-----------------------------------------------------')
        print('check if Requisition was created by current user')
        requisition_object = RequisitionForm.objects.get(pk=requisition)
        if requisition_object.created_by == request.user:
            return Response({"error": "You cannot approve/reject a Requisition you created"},
                            status=status.HTTP_400_BAD_REQUEST)

        print('-------------------------')
        print('Check if the Approvee is authorized to make an approval')
        authorization_instance = ApprovalAuthorization('requisition', requisition, request.user.id)

        if authorization_instance.approve_count_limit():
            return Response({"error": "Approvee already made an approval status"}, status=status.HTTP_400_BAD_REQUEST)
        if authorization_instance.form_approvals_count():
            return Response({"error": "Allowed number of Approvals exceeded"}, status=status.HTTP_400_BAD_REQUEST)

        print("-------------------------")
        print("Create an Approvee Object")
        approvee_object = Approvee()
        approvee_object.name = request.user
        approvee_object.approval_status = data['approval_status']

        if 'comment' in data:
            approvee_object.comment = data['comment']
        print("--------------------------------------------------")
        print("Assign Approvee Weights based on their permissions")
        if request.user.is_head_department:
            if data['approval_status']:
                approvee_object.weight = get_weight('is_head_department')
            else:
                approvee_object.weight = -abs(int(get_weight('is_head_department')))

        if request.user.is_procurement_committee:
            if data['approval_status']:
                approvee_object.weight = get_weight('is_procurement_committee')
            else:
                approvee_object.weight = -abs(int(get_weight('is_procurement_committee')))

        if request.user.is_procurement_officer:
            if data['approval_status']:
                approvee_object.weight = get_weight('is_procurement_officer')
            else:
                approvee_object.weight = -abs(int(get_weight('is_procurement_officer')))

        if request.user.is_head_of_finance:
            if data['approval_status']:
                approvee_object.weight = get_weight('is_head_finance')
            else:
                approvee_object.weight = -abs(int(get_weight('is_head_finance')))

        if request.user.is_ceo:
            if data['approval_status']:
                approvee_object.weight = get_weight('is_ceo')
            else:
                approvee_object.weight = -abs(int(get_weight('is_ceo')))
        approvee_object.save()

        requisition_instance = RequisitionForm.objects.get(pk=requisition)

        print("--------------------------------")
        print("Create A Requisition Approvee Instance")
        requisition_approvee = RequisitionFormApprovee()
        requisition_approvee.requisition = requisition_instance
        requisition_approvee.approvee = approvee_object
        requisition_approvee.save()

        print("---------------------")
        print("Updating Requisition Status")
        requisition_status = RequisitionFormStatus(requisition)
        print(requisition_status.get_all_approvee_weights())

        print("---------------------------")
        print("update status of the Quote")
        requisition = RequisitionForm.objects.get(pk=requisition)
        requisition.status = requisition_status.get_requisition_status()
        requisition.save()

        return Response({
            "success": "Requisition Approval Status Recorded",
            "status": status.HTTP_200_OK,
            "requisition": {
                "id": requisition.id,
                "status": requisition.status
            }
        })


class RequisitionFormApproveeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # Get The Approval Status of a User
    def get(self, request, requisition):
        if RequisitionFormApprovee.objects.filter(requisition__id=requisition,
                                                  approvee__name=request.user.id).exists():
            requisition_approvee = RequisitionFormApprovee.objects.get(requisition__id=requisition,
                                                                       approvee__name=request.user.id)
            return Response({
                "status": status.HTTP_200_OK,
                "approval_status": requisition_approvee.approvee.approval_status,
                "comment": requisition_approvee.approvee.comment,
                "approved_at": requisition_approvee.approvee.created_at
            })

        return Response({
            "status": status.HTTP_204_NO_CONTENT,
            "message": "No Approval Status Recorded"
        })

    # Update Approvee Details and Update Procurement Plan Overall Status
    def put(self, request, requisition):
        data = request.data
        print(data)

        if RequisitionFormApprovee.objects.filter(requisition__id=requisition,
                                                  approvee__name=request.user.id).exists():
            requisition_approvee = RequisitionFormApprovee.objects.get(requisition__id=requisition,
                                                                       approvee__name=request.user.id)
            approvee_id = requisition_approvee.approvee.id

            approvee_instance = Approvee.objects.get(pk=approvee_id)
            if 'approval_status' in data:
                approvee_instance.approval_status = data['approval_status']
            if 'comment' in data:
                approvee_instance.comment = data['comment']

            print("--------------------------------------------------")
            print("Assign Approvee Weights based on their permissions")
            if request.user.is_head_department:
                if data['approval_status']:
                    approvee_instance.weight = get_weight('is_head_department')
                else:
                    print(-abs(int(get_weight('is_head_department'))))
                    approvee_instance.weight = -abs(int(get_weight('is_head_department')))

            if request.user.is_procurement_committee:
                if data['approval_status']:
                    approvee_instance.weight = get_weight('is_procurement_committee')
                else:
                    approvee_instance.weight = -abs(int(get_weight('is_procurement_committee')))

            if request.user.is_procurement_officer:
                if data['approval_status']:
                    approvee_instance.weight = get_weight('is_procurement_officer')
                else:
                    approvee_instance.weight = -abs(int(get_weight('is_procurement_officer')))

            if request.user.is_head_of_finance:
                if data['approval_status']:
                    approvee_instance.weight = get_weight('is_head_finance')
                else:
                    approvee_instance.weight = -abs(int(get_weight('is_head_finance')))

            if request.user.is_ceo:
                if data['approval_status']:
                    approvee_instance.weight = get_weight('is_ceo')
                else:
                    approvee_instance.weight = -abs(int(get_weight('is_ceo')))

            approvee_instance.save()

            print("---------------------")
            print("Updating Requisition Status")
            requisition_status = RequisitionFormStatus(requisition)
            print(requisition_status.get_all_approvee_weights())

            print("---------------------------")
            print("update status of the Quote")
            requisition = RequisitionForm.objects.get(pk=requisition)
            requisition.status = requisition_status.get_requisition_status()
            requisition.save()

            return Response({
                "status": status.HTTP_200_OK,
                "approval_status": approvee_instance.approval_status,
                "comment": approvee_instance.comment
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "No record Found"
        })


class QuoteApproveeList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        data = request.data

        if not data['quote'] and data['quote_file']:
            return Response({"error": "Missing Quote"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        print('-------------------------')
        print('Check if the Approvee is authorized to make an approval')
        authorization_instance = ApprovalAuthorization('quote', data['quote'], request.user.id, data['quote_file'])

        if authorization_instance.approve_count_limit():
            return Response({"error": "Approvee already made an approval status"}, status=status.HTTP_400_BAD_REQUEST)
        if authorization_instance.form_approvals_count():
            return Response({"error": "Allowed number of Approvals exceeded"}, status=status.HTTP_400_BAD_REQUEST)

        print("-------------------------")
        print("Create an Approvee Object")
        approvee_object = Approvee()
        approvee_object.name = request.user
        approvee_object.approval_status = data['approval_status']

        if data['comment']:
            approvee_object.comment = data['comment']
        print("--------------------------------------------------")
        print("Assign Approvee Weights based on their permissions")
        if request.user.is_head_department:
            if data['approval_status']:
                approvee_object.weight = get_weight('is_head_department')
            else:
                print(-abs(int(get_weight('is_head_department'))))
                approvee_object.weight = -abs(int(get_weight('is_head_department')))

        if request.user.is_procurement_committee:
            if data['approval_status']:
                approvee_object.weight = get_weight('is_procurement_committee')
            else:
                approvee_object.weight = -abs(int(get_weight('is_procurement_committee')))

        if request.user.is_procurement_officer:
            if data['approval_status']:
                approvee_object.weight = get_weight('is_procurement_officer')
            else:
                approvee_object.weight = -abs(int(get_weight('is_procurement_officer')))

        if request.user.is_head_of_finance:
            if data['approval_status']:
                approvee_object.weight = get_weight('is_head_finance')
            else:
                approvee_object.weight = -abs(int(get_weight('is_head_finance')))

        if request.user.is_ceo:
            if data['approval_status']:
                approvee_object.weight = get_weight('is_ceo')
            else:
                approvee_object.weight = -abs(int(get_weight('is_ceo')))
        approvee_object.save()

        print("--------------------------------")
        print("Create A Quote Approvee Instance")
        QuoteApprovee.objects.create_quote_approvee(approvee_object, data['quote'], data['quote_file'])
        print("---------------------")
        print("Updating Quote Status")
        quote_status = QuoteStatus(data['quote'], data['quote_file'])
        print("Approvee weights", quote_status.get_all_approvee_weights())
        print("Quote File Status", quote_status.get_quote_status())

        print("---------------------------")
        print("update status of the Quote")
        quote_file = QuoteFile.objects.get(pk=data['quote_file'])
        quote_file.status = quote_status.get_quote_status()
        quote_file.save()

        print(quote_file.status)

        print('-----------------------------')
        print('generate Local Purchase Order')
        generatelpo = GenerateLPO(data['quote_file'], request.user)
        generatelpo.create_delete_local_purchase_order()

        return Response({
            "success": "Quote File Approval Status Recorded",
            "status": status.HTTP_200_OK,
            "quote_file": {
                "id": quote_file.id,
                "status": quote_file.status
            }
        })


class QuoteApproveeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, quote_id, quote_file_id):
        if QuoteApprovee.objects.filter(quote__id=quote_id,
                                        approvee__name=request.user.id, quote_file__id=quote_file_id).exists():
            quote_approvee = QuoteApprovee.objects.get(quote__id=quote_id,
                                                       approvee__name=request.user.id, quote_file__id=quote_file_id)
            return Response({
                "status": status.HTTP_200_OK,
                "approval_status": quote_approvee.approvee.approval_status,
                "comment": quote_approvee.approvee.comment,
                "approved_at": quote_approvee.approvee.created_at
            })

        return Response({
            "status": status.HTTP_204_NO_CONTENT,
            "message": "No Approval Status Recorded"
        })

    # Update Approvee Details and Update Procurement Plan Overall Status
    def put(self, request, quote_id, quote_file_id):
        data = request.data
        print(data)

        if QuoteApprovee.objects.filter(quote__id=quote_id,
                                        approvee__name=request.user.id, quote_file__id=quote_file_id).exists():
            quote_approvee = QuoteApprovee.objects.get(quote__id=quote_id,
                                                       approvee__name=request.user.id, quote_file__id=quote_file_id)
            approvee_id = quote_approvee.approvee.id

            approvee_instance = Approvee.objects.get(pk=approvee_id)
            if 'approval_status' in data:
                approvee_instance.approval_status = data['approval_status']
            if 'comment' in data:
                approvee_instance.comment = data['comment']
            print("--------------------------------------------------")
            print("Assign Approvee Weights based on their permissions")
            if request.user.is_head_department:
                if data['approval_status']:
                    approvee_instance.weight = get_weight('is_head_department')
                else:
                    print(-abs(int(get_weight('is_head_department'))))
                    approvee_instance.weight = -abs(int(get_weight('is_head_department')))

            if request.user.is_procurement_committee:
                if data['approval_status']:
                    approvee_instance.weight = get_weight('is_procurement_committee')
                else:
                    approvee_instance.weight = -abs(int(get_weight('is_procurement_committee')))

            if request.user.is_procurement_officer:
                if data['approval_status']:
                    approvee_instance.weight = get_weight('is_procurement_officer')
                else:
                    approvee_instance.weight = -abs(int(get_weight('is_procurement_officer')))

            if request.user.is_head_of_finance:
                if data['approval_status']:
                    approvee_instance.weight = get_weight('is_head_finance')
                else:
                    approvee_instance.weight = -abs(int(get_weight('is_head_finance')))

            if request.user.is_ceo:
                if data['approval_status']:
                    approvee_instance.weight = get_weight('is_ceo')
                else:
                    approvee_instance.weight = -abs(int(get_weight('is_ceo')))
            approvee_instance.save()

            print("---------------------")
            print("Get QuoteFile Status")
            quote_status = QuoteStatus('quote', quote_id, quote_file_id)
            print("Quote File Status", quote_status.get_all_approvee_weights())
            print("Quote File Status", quote_status.get_quote_status())

            print("---------------------")
            print("---------------------------")
            print("update status of the QuoteFile")
            quote_file = QuoteFile.objects.get(pk=quote_file_id)
            quote_file.status = quote_status.get_quote_status()
            quote_file.save()

            return Response({
                "status": status.HTTP_200_OK,
                "approval_status": approvee_instance.approval_status,
                "comment": approvee_instance.comment
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "No record Found"
        })


class ApproveeList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        approvee = Approvee.objects.all()
        serializer = ApproveeSerializer(approvee, many=True)
        return Response(serializer.data)


class ApproveeDetail(APIView):
    def get_object(self, pk):
        try:
            return Approvee.objects.get(pk=pk)
        except Approvee.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        approvee = self.get_object(pk)
        serializer = ApproveeSerializer(approvee)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        approvee = self.get_object(pk)
        serializer = ApproveeSerializer(approvee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        approvee = self.get_object(pk)
        approvee.delete()
        return Response({"Delete": "Successfully"}, status=status.HTTP_204_NO_CONTENT)
