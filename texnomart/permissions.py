from rest_framework import permissions
from datetime import datetime

class WeekdayOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        current_day = datetime.now().weekday()

        if current_day >= 5 and request.method in permissions.SAFE_METHODS:
            return False
        return True