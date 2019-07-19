from rest_framework import mixins, viewsets
from rest_framework.response import Response

from api.filters import UserFilter
from api.serializers import UserBasicSerializer, UserPostSerializer, UserUpdateSerializer, USER_NOT_EXISTS
from common.models import User
from utils.errors import ParamError


class UserView(viewsets.GenericViewSet,
                mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.DestroyModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin):

    queryset = User.objects.exclude(isDelete=True)
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
            # raise ParamError({'code': 2001, 'msg': '用户字段校验有误', 'error': list(serializers.errors.values())[0][0]})
            # {
            #     "code": 2001,
            #     "msg": "用户字段校验有误",
            #     "error": "昵称长度不要少于3个字符"
            # }
            raise ParamError({'code': 2001, 'msg': '用户字段校验有误', 'error': serializers.errors})
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
            raise ParamError({'code': 2001, 'msg': '字段校验有误', 'error': serializers.errors})
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
