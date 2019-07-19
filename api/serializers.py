from rest_framework import serializers
from rest_framework.response import Response

from common.models import User
from common.utils import get_uuid, TEL_PATTERN, EMAIL_PATTERN
from utils.conn import *
from utils.errors import ParamError


class UserBasicSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ('id', 'nickName', 'realName')


class UserPostSerializer(serializers.Serializer):

    gender_choices = (
        (1, "男"),
        (2, "女"),
        (3, "保密")
    )
    userID = serializers.CharField(max_length=64, required=True)
    nickName = serializers.CharField(min_length=3, max_length=10, required=True,
                                     error_messages={
                                         'min_length': '昵称长度不要少于3个字符',
                                         'max_length': '昵称长度不要大于10个字符',
                                         'required': '昵称不能为空'
                                     })
    email = serializers.CharField(max_length=255, required=True)
    realName = serializers.CharField(max_length=32, required=True)
    gender = serializers.ChoiceField(choices=gender_choices, required=False)
    tel = serializers.CharField(max_length=32, required=True)
    dateBirth = serializers.DateField(required=False)
    point = serializers.IntegerField(required=False)
    avatar = serializers.CharField(required=False)
    roles = serializers.ListField(child=serializers.CharField(required=False), required=False)

    def validate(self, attrs):
        # 逻辑校验
        if User.objects.filter(email=attrs['email']).exists():
            raise ParamError(USER_EMAIL_EXISTS)
        if not EMAIL_PATTERN.match(attrs['email']):
            raise ParamError(USER_EMAIL_ERROR)
        if User.objects.filter(tel=attrs['tel']).exists():
            raise ParamError(USER_TEL_EXISTS)
        if not TEL_PATTERN.match(attrs['tel']):
            raise ParamError(USER_TEL_ERROR)
        return attrs


    def create_user(self, validated_data):
        validated_data['uuid'] = get_uuid()
        user = User.objects.create(**validated_data)
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

    nickName = serializers.CharField(max_length=32, required=True)
    email = serializers.CharField(max_length=255, required=True)
    gender = serializers.ChoiceField(choices=gender_choices, required=False)
    avatar = serializers.CharField(required=False)


    def validate(self, attrs):
        # 逻辑校验
        return attrs

    def update_user(self, instance, validate_data):
        instance.gender = validate_data['gender']
        instance.nickName = validate_data['nickName']
        instance.email = validate_data['email']
        instance.avatar = validate_data.get('avatar')
        instance.save()

        res = {
            'user': UserBasicSerializer(instance).data
        }
        return res



