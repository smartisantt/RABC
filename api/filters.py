import django_filters

from common.models import User, Role, Permissions


class UserFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = ('id', 'uuid', 'nickName')


class RoleFilter(django_filters.FilterSet):

    class Meta:
        model = Role
        fields = ('id', 'uuid', 'roleName')


class PermissionsFilter(django_filters.FilterSet):

    class Meta:
        model = Permissions
        fields = ('id', 'uuid', 'permissionName')

