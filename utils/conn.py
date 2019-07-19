
SUCCESS = {'code': 200, 'msg': 'OK'}

# 用户模块
USER_NOT_EXISTS = {'code': 1001, 'msg': '用户不存在'}
USER_EMAIL_EXISTS = {'code': 1002, 'msg': '邮箱重复'}
USER_EMAIL_ERROR = {'code': 1003, 'msg': '邮箱格式错误'}
USER_TEL_EXISTS = {'code': 1004, 'msg': '电话号码重复'}
USER_TEL_ERROR = {'code': 1005, 'msg': '电话号码格式错误'}



USER_PASSWORD_ERROR = {'code': 1002, 'msg': '账号或密码错误，请确认登录信息'}
USER_REGISTER_EXISTS = {'code': 1003, 'msg': '注册账号已存在，请更换账号'}
USER_PASSWORD_NOT_EQUAL = {'code': 1004, 'msg': '注册密码和确认密码不一致'}
