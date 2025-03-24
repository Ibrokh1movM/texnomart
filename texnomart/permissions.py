from rest_framework import permissions
from datetime import datetime


class WeekdayOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        current_day = datetime.now().weekday()
        if current_day >= 5 and request.method in permissions.SAFE_METHODS:
            return False
        return True


class IsCommentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return True
        # Agar foydalanuvchi autentifikatsiya qilinmagan bo'lsa, faqat o'zi qo'shgan sharhlar uchun ruxsat
        return obj.user == request.user if request.user.is_authenticated else False
