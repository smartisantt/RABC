from rest_framework import serializers
from rest_framework.response import Response

from common.models import User, Role, Permissions
from common.utils import get_uuid, TEL_PATTERN, EMAIL_PATTERN
from utils.conn import *
from utils.errors import ParamError


class UserBasicSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    @staticmethod
    def get_roles(user):
        return RoleSimpleSerializer(user.roles, many=True).data

    class Meta:
        model = User
        fields = ('uuid', 'nickName', 'realName', 'roles')


class UserPostSerializer(serializers.Serializer):
    gender_choices = (
        (1, "男"),
        (2, "女"),
        (3, "保密")
    )
    userID = serializers.CharField(max_length=64, required=True,
                                   error_messages={
                                       'required': 'userID必填'
                                   }
                                   )
    nickName = serializers.CharField(min_length=3, max_length=10, required=True,
                                     error_messages={
                                         'min_length': '昵称长度不要少于3个字符',
                                         'max_length': '昵称长度不要大于10个字符',
                                         'required': '昵称必填'
                                     })
    email = serializers.CharField(max_length=255, required=True,
                                  error_messages={
                                      'required': '邮箱必填'
                                  })
    realName = serializers.CharField(min_length=2, max_length=5, required=True,
                                     error_messages={
                                         'min_length': '名字长度不要小于2个字',
                                         'max_length': '名字长度不要大于5个字',
                                         'required': '真实名字必填'
                                     })
    gender = serializers.ChoiceField(choices=gender_choices, required=False)
    tel = serializers.CharField(max_length=32, required=True, error_messages={'required': '电话必填'})
    dateBirth = serializers.DateField(required=False)
    point = serializers.IntegerField(required=False)
    avatar = serializers.CharField(required=False)

    roles = serializers.SlugRelatedField(many=True,
                                         slug_field="uuid",
                                         queryset=Role.objects.filter(isDelete=False),
                                         required=True,
                                         error_messages={
                                             'required': "角色不能为空"
                                         })

    def validate(self, attrs):
        # 逻辑校验
        if User.objects.filter(email=attrs['email'], isDelete=False).exists():
            raise ParamError(USER_EMAIL_EXISTS)
        if not EMAIL_PATTERN.match(attrs['email']):
            raise ParamError(USER_EMAIL_ERROR)
        if User.objects.filter(tel=attrs['tel'], isDelete=False).exists():
            raise ParamError(USER_TEL_EXISTS)
        if not TEL_PATTERN.match(attrs['tel']):
            raise ParamError(USER_TEL_ERROR)
        return attrs


    def create_user(self, validated_data):
        roles = validated_data.pop('roles')
        validated_data['uuid'] = get_uuid()
        user = User.objects.create(**validated_data)
        roles = Role.objects.filter(uuid__in=roles).all()
        user.roles.add(*roles)
        res = {
            'user': UserBasicSerializer(user).data
        }
        return res


class UserUpdateSerializer(serializers.Serializer):
    gender_choices = (
        (1, "男"),
        (2, "女"),
        (3, "保密")
    )

    nickName = serializers.CharField(min_length=3, max_length=10, required=True,
                                     error_messages={
                                         'min_length': '昵称长度不要少于3个字符',
                                         'max_length': '昵称长度不要大于10个字符',
                                         'required': '昵称必填'
                                     })
    email = serializers.CharField(max_length=255, required=True,
                                  error_messages={
                                      'required': '邮箱必填'
                                  })
    gender = serializers.ChoiceField(choices=gender_choices, required=False)
    avatar = serializers.CharField(required=False)
    # roles = serializers.ListField(child=serializers.CharField(required=False), required=False)
    roles = serializers.SlugRelatedField(many=True,
                                         slug_field="uuid",
                                         queryset=Role.objects.filter(isDelete=False),
                                         required=True,
                                         error_messages={
                                             'required': "角色不能为空"
                                         })

    def update_user(self, instance, validate_data):
        instance.gender = validate_data.get('gender', instance.gender)
        instance.avatar = validate_data.get('avatar', instance.avatar)
        instance.nickName = validate_data['nickName']
        qs = User.objects.filter(email=validate_data['email'], isDelete=False).exclude(uuid=instance.uuid)
        if qs.exists():
            raise ParamError(USER_EMAIL_EXISTS)
        instance.email = validate_data['email']

        roles = Role.objects.filter(uuid__in=validate_data.get('roles')).all()
        instance.roles.clear()
        instance.roles.add(*roles)
        instance.save()

        res = {
            'user': UserBasicSerializer(instance).data
        }
        return res


"""角色"""
class RoleSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ('uuid', 'roleName', 'roleCode')


class RoleBasicSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    @staticmethod
    def get_permissions(role):
        # permissions = role.permissions.filter(isDelete=False).all()
        return PermissionsBasicSerializer(role.permissions, many=True).data

    class Meta:
        model = Role
        fields = ('uuid', 'roleName', 'roleCode', 'permissions')


class RolePostSerializer(serializers.Serializer):
    roleName = serializers.CharField(min_length=2, max_length=12, required=True,
                                     error_messages={
                                         'min_length': '角色名字不要小于2个字',
                                         'max_length': '角色名字不要大于12个字',
                                         'required': '角色名字必填'
                                     })
    roleCode = serializers.CharField(min_length=2, max_length=12, required=True,
                                     error_messages={
                                         'min_length': '角色编码不要小于2个字',
                                         'max_length': '角色编码不要大于12个字',
                                         'required': '角色编码必填'
                                     })
    # permissions = serializers.ListField(child=serializers.CharField(required=False), required=True)
    permissions = serializers.SlugRelatedField(many=True,
                                               slug_field="uuid",
                                               required=True,
                                               queryset=Permissions.objects.filter(isDelete=False),
                                               error_messages={
                                                   'required': '权限不能为空'
                                               })

    def validate(self, attrs):
        if Role.objects.filter(roleName=attrs['roleName'], isDelete=False).exists():
            raise ParamError(ROLE_NAME_EXISTS)
        if Role.objects.filter(roleCode=attrs['roleCode'], isDelete=False).exists():
            raise ParamError(ROLE_CODE_EXISTS)
        return attrs

    def create_role(self, validated_data):
        permissions = validated_data.pop('permissions')
        validated_data['uuid'] = get_uuid()
        role = Role.objects.create(**validated_data)
        permissions = Permissions.objects.filter(uuid__in=permissions).all()        # 这里可以不用过滤isDelete=False
        role.permissions.add(*permissions)

        res = {
            'role': RoleBasicSerializer(role).data
        }
        return res


class RoleUpdateSerializer(serializers.Serializer):
    roleName = serializers.CharField(min_length=2, max_length=12, required=True,
                                     error_messages={
                                         'min_length': '角色名字不要小于2个字',
                                         'max_length': '角色名字不要大于12个字',
                                         'required': '角色名字必填'
                                     })
    roleCode = serializers.CharField(min_length=2, max_length=12, required=True,
                                     error_messages={
                                         'min_length': '角色编码不要小于2个字',
                                         'max_length': '角色编码不要大于12个字',
                                         'required': '角色编码必填'
                                     })
    # permissions = serializers.ListField(child=serializers.CharField(required=False), required=True)
    permissions = serializers.SlugRelatedField(many=True,
                                               slug_field="uuid",
                                               required=True,
                                               queryset=Permissions.objects.filter(isDelete=False),
                                               error_messages={
                                                   'required': '权限不能为空'
                                               })

    def update_role(self, instance, validate_data):
        qs = Role.objects.filter(roleName=validate_data['roleName'], isDelete=False).exclude(uuid=instance.uuid)
        if qs.exists():
            raise ParamError(ROLE_NAME_EXISTS)
        qs = Role.objects.filter(roleCode=validate_data['roleCode'], isDelete=False).exclude(uuid=instance.uuid)
        if qs.exists():
            raise ParamError(ROLE_CODE_EXISTS)

        instance.roleName = validate_data['roleName']
        instance.roleCode = validate_data['roleCode']
        permissions = Permissions.objects.filter(uuid__in=validate_data.get('permissions'), isDelete=False).all()
        instance.permissions.clear()
        instance.permissions.add(*permissions)
        instance.save()

        res = {
            'permission': RoleBasicSerializer(instance).data
        }
        return res


class PermissionsBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permissions
        fields = ('uuid', 'permissionName', 'permissionCode')


class PermissionPostSerializer(serializers.Serializer):
    permissionName = serializers.CharField(min_length=2, max_length=12, required=True,
                                           error_messages={
                                             'min_length': '权限名字不要小于2个字',
                                             'max_length': '权限名字不要大于12个字',
                                             'required': '权限名字必填'
                                         })
    permissionCode = serializers.CharField(min_length=2, max_length=12, required=True,
                                           error_messages={
                                             'min_length': '权限编码不要小于2个字',
                                             'max_length': '权限编码不要大于12个字',
                                             'required': '权限编码必填'
                                         })

    def validate(self, attrs):
        if Permissions.objects.filter(permissionName=attrs['permissionName'], isDelete=False).exists():
            raise ParamError(PERMISSION_NAME_EXISTS)
        if Permissions.objects.filter(permissionCode=attrs['permissionCode'], isDelete=False).exists():
            raise ParamError(PERMISSION_CODE_EXISTS)
        return attrs

    def create_permission(self, validated_data):
        validated_data['uuid'] = get_uuid()
        permission = Permissions.objects.create(**validated_data)
        res = {
            'permission': PermissionsBasicSerializer(permission).data
        }
        return res


class PermissionUpdateSerializer(serializers.Serializer):
    permissionName = serializers.CharField(min_length=2, max_length=12, required=True,
                                           error_messages={
                                             'min_length': '权限名字不要小于2个字',
                                             'max_length': '权限名字不要大于12个字',
                                             'required': '权限名字必填'
                                            })
    permissionCode = serializers.CharField(min_length=2, max_length=12, required=True,
                                           error_messages={
                                                 'min_length': '权限编码不要小于2个字',
                                                 'max_length': '权限编码不要大于12个字',
                                                 'required': '权限编码必填'
                                            })

    def update_permission(self, instance, validate_data):
        qs = Permissions.objects.filter(permissionName=validate_data['permissionName'], isDelete=False).\
            exclude(uuid=instance.uuid)
        if qs.exists():
            raise ParamError(PERMISSION_NAME_EXISTS)
        qs = Permissions.objects.filter(permissionCode=validate_data['permissionCode'], isDelete=False).\
            exclude(uuid=instance.uuid)
        if qs.exists():
            raise ParamError(PERMISSION_CODE_EXISTS)

        instance.permissionName = validate_data['permissionName']
        instance.permissionCode = validate_data['permissionCode']
        instance.save()

        res = {
            'permission': PermissionsBasicSerializer(instance).data
        }
        return res

