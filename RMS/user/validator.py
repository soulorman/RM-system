# encoding: utf-8
from django.utils import timezone
from .models import User
import hashlib

def encrypt_password(password: str) -> str:
    """加密用户的密码

    md5加密用户密码
    : param password:明文密码
    : return : 加密后的密码
    """
    if not isinstance(password, bytes):
        password = str(password).encode()

    md5 = hashlib.md5()
    md5.update(password)
    
    return md5.hexdigest()


class UserValiator(object):

    @classmethod
    def valid_login(cls, name, password):
        """认证用户名/密码

        : param name:用户名
        : param password:密码
        : return: 验证成功返回用户信息，验证错误返回None
        """
        user = None
        try:
            user = User.objects.get(name=name)
        except:
            return None
        
        password = encrypt_password(password)
        if user.password == password:
            return user

        return None

    @classmethod
    def valid_create(cls, params):
        """验证创建的用户

        :param params: 创建的用户所有信息
        :return: 返回验证信息，用户信息，错误信息
        """
        is_valid = True
        errors = {}
        user = User()
    
        user.name = params.get('name', '').strip()
        if user.name == '':
            is_valid = False
            errors['name'] = '用户名不能为空'
        else:
            try:
                User.objects.get(name=user.name)
                is_valid = False
                errors['name'] = '用户名已存在'
            except BaseException as e:
                pass

        user.password = params.get('password', '').strip()
        user.password_new = params.get('password_new', '').strip()
        if user.password == '' or user.password != user.password_new:
            is_valid = False
            errors['password'] = '密码不能为空,且两次密码不匹配'
        else:
            user.password = encrypt_password(user.password)

        user.age = params.get('age', '0').strip()
        user.create_time = timezone.now()

        return is_valid, user, errors



    @classmethod 
    def valid_changepass(cls, params):
        """验证密码

        :param param:传入2个密码
        :return: 返回验证信息，用户信息，错误信息
        """
        is_valid = True
        errors = {}
        user = None

        try:
            user = User.objects.get(pk=params.get('id', '').strip())
        except BaseException as e:
            is_valid = False
            errors['id'] = '用户信息不存在'
            return is_valid, user, errors

        password = params.get('password', '').strip()
        if user.password != encrypt_password(password):
            is_valid = False
            errors['password'] = '密码认证失败'

        password_new = params.get('password_new', '').strip()
        password_new_1 = params.get('password_new_1', '').strip()
        if password_new == '' or password_new_1 == '':
            is_valid = False
            errors['password_new'] = '新密码不能为空'
        elif password_new != password_new_1:
            is_valid = False
            errors['password_new'] = '新密码不匹配'
        else:
            user.password = encrypt_password(password_new)

        return is_valid, user, errors