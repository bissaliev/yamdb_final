from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    """ Доступ только для админов или суперюзеров. """

    def has_permission(self, request, view):

        return (
            request.user.is_admin
            if request.user.is_authenticated else False
        )


class ISAdminOnlyEdit(permissions.BasePermission):
    """ Доступ только для админов или суперюзеров. """

    def has_permission(self, request, view):

        return (
            request.user.is_admin
            if request.user.is_authenticated
            else request.method in permissions.SAFE_METHODS
        )


class ISAdminAuthorOrSuperuser(permissions.BasePermission):
    """
    Get - все пользователи
    Post - все авторизованные
    Все оставшиеся - только административный персонал и автор.
    """

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):

        return (
            request.user == obj.author
            or request.user.is_admin
            or request.user.is_moderator
            if request.user.is_authenticated
            else request.method in permissions.SAFE_METHODS
        )
