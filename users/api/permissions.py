from rest_framework import permissions

class IsMedico(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Medicos").exists()
    
    