from django.db import models
from datetime import datetime


class Base(models.Model):
    create_at = models.DateTimeField(default = datetime.now)  # 创建时间
    update_at = models.DateTimeField(default = datetime.now)  # 修改时间

    class Meta:
        abstract = True


# 网站cookie模型
class Site_Cookie(Base):
    userid = models.CharField(max_length = 32, verbose_name = '用户ID',default = '1')
    sitename = models.CharField(max_length = 50)  # 网站名
    siteaddress = models.CharField(max_length = 150)  # 网站地址
    username = models.CharField(max_length = 150)  # 网站用户名
    password_hash = models.CharField(max_length = 100)  # 密码
    password_salt = models.CharField(max_length = 50)  # 密码干扰值
    site_cookie = models.CharField(max_length = 500)  # 网站cookie值
    status = models.IntegerField(default = 1)  # 状态:1正常/2禁用/9删除

    def toDict(self):
        return {'id': self.id, 'userid': self.userid, 'sitename': self.sitename, 'siteaddress': self.siteaddress,
                'username': self.username,
                'password_hash': self.password_hash, 'password_salt': self.password_salt,
                'site_cookie': self.site_cookie,
                'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "site_cookie"  # 更改表名


class User(Base):
    username = models.CharField(max_length = 50)  # 账号
    phone_number = models.CharField(max_length = 11, null = True)  # 手机号
    email = models.CharField(max_length = 50, null = True)  # 邮箱
    password_hash = models.CharField(max_length = 100)  # 密码
    password_salt = models.CharField(max_length = 50)  # 密码干扰值
    status = models.IntegerField(default = 1)  # 状态:1正常/2禁用/6管理员/9删除
    create_at = models.DateTimeField(default = datetime.now)  # 创建时间
    update_at = models.DateTimeField(default = datetime.now)  # 修改时间

    def toDict(self):
        return {'id': self.id, 'username': self.username, 'phone_number': self.phone_number, 'email': self.email,
                'password_hash': self.password_hash, 'password_salt': self.password_salt, 'status': self.status,
                'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "user"  # 更改表名
        unique_together = ('username', 'phone_number', 'email')

    # class Spider(models.Model):
#     username = models.CharField(max_length = 50)  # 账号
#     password_hash = models.CharField(max_length = 100)  # 密码
#     password_salt = models.CharField(max_length = 50)  # 密码干扰值
#     status = models.IntegerField(default = 1)  # 状态:1正常/2禁用/6管理员/9删除
#     create_at = models.DateTimeField(default = datetime.now)  # 创建时间
#     update_at = models.DateTimeField(default = datetime.now)  # 修改时间
#
#     def toDict(self):
#         return {'id': self.id, 'username': self.username,
#                 'password_hash': self.password_hash, 'password_salt': self.password_salt, 'status': self.status,
#                 'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
#                 'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}
#
#     class Meta:
#         db_table = "spider"  # 更改表名
