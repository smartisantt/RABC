from rest_framework import mixins, viewsets
from rest_framework.response import Response

from api.filters import UserFilter, RoleFilter, PermissionsFilter
from api.serializers import *
from common.models import User, Role
from utils.errors import ParamError


class UserView(viewsets.GenericViewSet,
               mixins.CreateModelMixin,
               mixins.ListModelMixin,
               mixins.DestroyModelMixin,
               mixins.UpdateModelMixin,
               mixins.RetrieveModelMixin):

    queryset = User.objects.exclude(isDelete=True).prefetch_related('roles')
    serializer_class = UserBasicSerializer
    filter_class = UserFilter

    lookup_field = 'uuid'

    """
    GET     /api/user/              获取所有用户
    GET     /api/user/<str:uuid>/   获取单个用户
    POST    /api/user/              创建用户
    PUT     /api/user/<str:uuid>/   修改用户
    DELETE  /api/user/<str:uuid>/   删除用户
    """
    def create(self, request, *args, **kwargs):
        # 增
        serializers = UserPostSerializer(data=request.data)
        result = serializers.is_valid(raise_exception=False)
        if not result:
            raise ParamError({'code': 2001, 'msg':list(serializers.errors.values())[0][0]})
            # raise ParamError({'code': 2001, 'msg': '用户字段校验有误', **serializers.errors})
        data = serializers.create_user(serializers.data)
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        # 删
        try:
            instance = self.get_object()
        except Exception as e:
            raise ParamError(USER_NOT_EXISTS)
        instance.isDelete = True
        instance.save()
        serializers = UserBasicSerializer(instance)
        return Response(serializers.data)

    def update(self, request, *args, **kwargs):
        # 改
        try:
            instance = self.get_object()
        except Exception as e:
            raise ParamError(USER_NOT_EXISTS)
        serializers = UserUpdateSerializer(data=request.data)
        result = serializers.is_valid(raise_exception=False)
        if not result:
            raise ParamError({'code': 2001, 'msg': list(serializers.errors.values())[0][0]})
        data = serializers.update_user(instance, serializers.data)
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        # 查
        try:
            instance = self.get_object()
        except Exception as e:
            raise ParamError(USER_NOT_EXISTS)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class RoleView(viewsets.GenericViewSet,
               mixins.CreateModelMixin,
               mixins.ListModelMixin,
               mixins.DestroyModelMixin,
               mixins.UpdateModelMixin,
               mixins.RetrieveModelMixin):

    queryset = Role.objects.exclude(isDelete=True).prefetch_related('permissions')
    serializer_class = RoleBasicSerializer
    filter_class = RoleFilter

    lookup_field = 'uuid'

    def create(self, request, *args, **kwargs):
        # 增
        serializers = RolePostSerializer(data=request.data)
        result = serializers.is_valid(raise_exception=False)
        if not result:
            raise ParamError({'code': 2001, 'msg':list(serializers.errors.values())[0][0]})
            # raise ParamError({'code': 2001, 'msg': '用户字段校验有误', **serializers.errors})
        data = serializers.create_role(serializers.data)
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        # 删
        try:
            instance = self.get_object()
        except Exception as e:
            raise ParamError(ROLE_NOT_EXISTS)
        instance.isDelete = True
        users = User.objects.filter(isDelete=False).all()
        instance.user.remove(*users)
        # 删除中间表数据， 删除角色的时候，用户关联的角色的中间表也被删除
        instance.save()
        serializers = RoleBasicSerializer(instance)
        return Response(serializers.data)

    def update(self, request, *args, **kwargs):
        # 改
        try:
            instance = self.get_object()
        except Exception as e:
            raise ParamError(ROLE_NOT_EXISTS)
        serializers = RoleUpdateSerializer(data=request.data)
        result = serializers.is_valid(raise_exception=False)
        if not result:
            raise ParamError({'code': 2001, 'msg': list(serializers.errors.values())[0][0]})
        data = serializers.update_role(instance, serializers.data)
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        # 查
        try:
            instance = self.get_object()
        except Exception as e:
            raise ParamError(ROLE_NOT_EXISTS)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

"""权限"""


class PermissionsView(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin):

    queryset = Permissions.objects.exclude(isDelete=True)
    serializer_class = PermissionsBasicSerializer
    filter_class = PermissionsFilter

    lookup_field = 'uuid'

    def create(self, request, *args, **kwargs):
        # 增
        serializers = PermissionPostSerializer(data=request.data)
        result = serializers.is_valid(raise_exception=False)
        if not result:
            raise ParamError({'code': 2001, 'msg':list(serializers.errors.values())[0][0]})
            # raise ParamError({'code': 2001, 'msg': '用户字段校验有误', **serializers.errors})
        data = serializers.create_permission(serializers.data)
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        # 删
        try:
            instance = self.get_object()
        except Exception as e:
            raise ParamError(PERMISSION_NOT_EXISTS)
        instance.isDelete = True
        roles = Role.objects.filter(isDelete=False).all()
        instance.role.remove(*roles)
        instance.save()
        serializers = PermissionsBasicSerializer(instance)
        return Response(serializers.data)

    def update(self, request, *args, **kwargs):
        # 改
        try:
            instance = self.get_object()
        except Exception as e:
            raise ParamError(PERMISSION_NOT_EXISTS)
        serializers = PermissionUpdateSerializer(data=request.data)
        result = serializers.is_valid(raise_exception=False)
        if not result:
            raise ParamError({'code': 2001, 'msg': list(serializers.errors.values())[0][0]})
        data = serializers.update_permission(instance, serializers.data)
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        # 查
        try:
            instance = self.get_object()
        except Exception as e:
            raise ParamError(PERMISSION_NOT_EXISTS)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

