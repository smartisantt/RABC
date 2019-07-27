from django.db import models

from common.utils import get_uuid


class BaseModle(models.Model):
    uuid = models.CharField(max_length=64, unique=True, default=get_uuid())
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", null=True)
    updateTime = models.DateTimeField(auto_now=True, verbose_name="更新时间", null=True)

    class Meta:
        abstract = True


class Permissions(BaseModle, models.Model):
    permissionName = models.CharField(max_length=128, verbose_name="权限名称", blank=True, null=True)
    permissionCode = models.CharField(max_length=128, verbose_name="权限编码", blank=True, null=True)
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'tb_permissions'

    def __str__(self):
        return self.permissionName


class Role(BaseModle, models.Model):
    roleName = models.CharField(max_length=128, verbose_name="角色名称", blank=True, null=True)
    roleCode = models.CharField(max_length=128, verbose_name="角色编码", blank=True, null=True)
    isDelete = models.BooleanField(default=False)
    permissions = models.ManyToManyField(Permissions, related_name='role')

    class Meta:
        db_table = 'tb_role'

    def __str__(self):
        return self.roleName


# class RolesPermissions(BaseModle, models.Model):
#     """角色权限中间实体"""
#     permission = models.ForeignKey(Permissions, models.CASCADE, blank=True, null=True)
#     role = models.ForeignKey(Role, models.CASCADE, blank=True, null=True)
#
#     class Meta:
#         db_table = 'tb_roles_permissions'
#         unique_together = (('permission', 'role'),)


class User(BaseModle, models.Model):
    gender_choices = (
        (1, "男"),
        (2, "女"),
        (3, "保密")
    )

    userID = models.CharField(max_length=64, default=None)
    nickName = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    realName = models.CharField(max_length=32, blank=True, null=True)
    gender = models.IntegerField(choices=gender_choices, default=3)
    tel = models.CharField(max_length=32, blank=True, null=True)
    dateBirth = models.DateField(verbose_name="出生日期", blank=True, null=True)
    point = models.IntegerField(verbose_name="用户积分", default=0)
    lastVist = models.DateTimeField(verbose_name="上次访问时间", blank=True, null=True)
    avatar = models.CharField(verbose_name="用户头像", max_length=256, blank=True, null=True)
    isDelete = models.BooleanField(default=False)
    roles = models.ManyToManyField(Role, related_name='user')

    class Meta:
        db_table = 'tb_user'

    def __str__(self):
        return self.nickName


# class UsersRoles(BaseModle, models.Model):
#     """用户角色中间实体"""
#     role = models.ForeignKey(Role, models.CASCADE, blank=True, null=True)
#     user = models.ForeignKey(User, models.CASCADE, blank=True, null=True)
#
#     class Meta:
#         db_table = 'tb_users_roles'
#         unique_together = (('user', 'role'),)
