from rest_framework import serializers
from .models import Department, DEPARTMENT_NAMES
from authentication.models import User


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name']
4