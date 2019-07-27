from django.core.cache import caches
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

from common.models import User


class CustomAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            raise AuthenticationFailed('校验用户失败')
        # if not token:
        #     raise AuthenticationFailed('提供有效的身份认证标识')

        # 根据token获取当前登录用户
        user = User.objects.filter(uuid="8978DE2D92F1467D961341780B40987A").first()

        return user, token


class CustomAuthorization(BasePermission):
    message = '你没有权限'
    def has_permission(self, request, view):
        # 当前用户的权限缓存
        if not caches['default'].get(request.user.userID):
            permission_list = []
            for role in request.user.roles.all():
                for permission in role.permissions.all():
                    permission in permission_list or permission_list.append(permission)
            caches['default'].set(request.user.userID, permission_list)
        return True