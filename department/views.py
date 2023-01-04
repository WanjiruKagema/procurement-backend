from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import DepartmentSerializer
from .models import Department
from django.http import Http404
from rest_framework import permissions


# Create your views here.
# Department Function Based Views
class DepartmentList(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        if request.user.is_head_of_finance or request.user.is_procurement_officer or request.user.is_procurement_committee or request.user.is_ceo:
            department = Department.objects.all()
        if request.user.is_head_department or request.user.is_staff:
            department = Department.objects.filter(department_name=request.user.department)
        if request.user.is_staff:
            department = Department.objects.filter(department_name=request.user.department)
        serializer = DepartmentSerializer(department, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        department = self.get_object(pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
