from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        return False


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='Staff'):
            return True
        return False


class IsProcurementCommittee(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='ProcurementCommittee'):
            return True
        return False


class IsProcurementOfficer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_procurement_officer:
            return True
        return False


class IsHeadFinance(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_head_of_finance:
            return True
        return False


class IsHeadOfDepartment(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_head_department:
            return True
        return False
