import django_filters

from common.models import User, Role


class UserFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = ('uuid', 'nickName')

class RoleFilter(django_filters.FilterSet):

    class Meta:
        model = Role
        fields = ('uuid', 'roleName')

