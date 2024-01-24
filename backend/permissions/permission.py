from rest_framework import permissions

class SuperAdminLevelPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superadmin:
            return True
        
        return False
    
class AdminLevelPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_authenticated and (request.user.is_admin or request.user.is_superadmin):
            return True
        
        return False
    
class EmployeeLevelPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_authenticated and (request.user.is_admin or request.user.is_superadmin or request.user.is_employee):
            return True
        
        return False
    
class CustomerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve', 'partial_update', 'destroy']:
            return request.user.is_authenticated() and (request.user.is_admin or request.user.is_superadmin)
        elif view.action in ['create', 'partial_update']:
            return request.user.is_authenticated() and request.user.is_customer
        else:
            return False