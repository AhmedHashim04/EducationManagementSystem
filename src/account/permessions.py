from rest_framework.permissions import BasePermission




class IsStudent(BasePermission):
    """
    Allows access only to authenticated student users.
    """

    def has_permission(self, request, view):

        return bool(request.user and request.user.is_authenticated \
                    and request.user.profile.role == 'student' )

class IsInstructor(BasePermission):
    """
    Allows access only to authenticated instructor users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated \
                    and request.user.profile.role == 'instructor' )


