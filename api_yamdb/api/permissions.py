from rest_framework import permissions


class IsAdministrator(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_administrator or request.user.is_superuser
        )


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_moderator or request.user.is_superuser
        )


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous and (
            request.method not in permissions.SAFE_METHODS
        ):
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class ModeratorOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return True


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_administrator or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_administrator))


class IsAuthorizedOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous and (
            request.method not in permissions.SAFE_METHODS
        ):
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return True


class IsAuthorAdminAndModeratorOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'PATCH' and request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user or request.user.is_superuser
            or request.user.is_moderator
        )


class AuthUserAndAuthorAndSuperuserDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE' and request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user or request.user.is_superuser
            or request.user.is_moderator
        )


class ReviewCommentViewSetPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'partial_update':
            if request.method == 'PATCH' and request.user.is_authenticated:
                return True
        elif view.action == 'destroy':
            if request.method == 'DELETE' and request.user.is_authenticated:
                return True
        else:
            if request.user.is_anonymous and (
                request.method not in permissions.SAFE_METHODS
            ):
                return False
            return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'partial_update':
            return (
                obj.author == request.user or request.user.is_superuser
                or request.user.is_moderator
            )

        elif view.action == 'destroy':
            return (
                obj.author == request.user or request.user.is_superuser
                or request.user.is_moderator
            )
        else:
            if request.method in permissions.SAFE_METHODS:
                return True
            return True
