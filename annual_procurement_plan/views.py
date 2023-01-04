from django.shortcuts import render
from .models import ProcurementPlan
from .serializers import ProcurementPlanSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from authentication import permissions


# Create your views here.

class ProcurementPlanList(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        if request.user.is_head_department:
            procurement_plan = ProcurementPlan.objects.filter(department=request.user.department).order_by('id')
            serializer = ProcurementPlanSerializer(procurement_plan, many=True)
            return Response(serializer.data)
        procurement_plan = ProcurementPlan.objects.all().order_by('id')
        serializer = ProcurementPlanSerializer(procurement_plan, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProcurementPlanSerializer(data=request.data)
        if serializer.is_valid():
            procurement_plan = serializer.save()
            procurement_plan.created_by = request.user
            procurement_plan.department = request.user.department
            procurement_plan.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProcurementPlanDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return ProcurementPlan.objects.get(pk=pk)
        except ProcurementPlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        procurement_plan = self.get_object(pk)
        serializer = ProcurementPlanSerializer(procurement_plan)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ProcurementPlanSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        procurement_plan = self.get_object(pk)
        procurement_plan.delete()
        procurement_plans = ProcurementPlan.objects.get_queryset()
        serializer = ProcurementPlanSerializer(procurement_plans, many=True)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)