import django_filters

from common.models import User


class UserFilter(django_filters.FilterSet):


    class Meta:
        model = User
        fields = ('uuid', 'nickName')