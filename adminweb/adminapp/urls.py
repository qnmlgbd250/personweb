# -*- coding: utf-8 -*-
# @Time    : 2022/3/27 9:22
# @Author  : huni
# @Email   : zcshiyonghao@163.com
# @File    : urls.py
# @Software: PyCharm
from django.contrib import admin
from django.urls import path, include
from .views import index,op_cookie

urlpatterns = [
    # 后台管理首页
    path('', index.index, name = 'index'),

    # 网站登录注册
    path('login', index.login, name = 'login'),  # 加载登录表单
    path('register', index.register, name = 'register'),  # 加载登录表单
    path('doregister', index.doregister, name = 'doregister'),  # 加载登录表单
    path('dologin', index.dologin, name = 'dologin'),  # 执行登录
    path('logout', index.logout, name = 'logout'),  # 执行退出
    path('verify', index.verify, name = 'verify'),  # 输出验证码

    # 网站cookie操作
    path('select_site/<int:page>_<int:per_page>', op_cookie.select_site, name = 'select_site'),
    path('add_cookie', op_cookie.add_cookie, name = 'add_cookie'),
    path('insert_cookie', op_cookie.insert_cookie, name = 'insert_cookie'),  # 执行添加
    path('edit_cookie/<int:siteid>', op_cookie.edit_cookie, name = 'edit_cookie'),
    path('get_cookie/<int:siteid>', op_cookie.get_cookie, name = 'get_cookie'),
    path('del_cookie/<int:siteid>', op_cookie.del_cookie, name = 'del_cookie'),
    path('batch_del_cookie', op_cookie.batch_del_cookie, name = 'batch_del_cookie'),
    path('update_cookie/<int:siteid>', op_cookie.update_cookie, name = 'update_cookie'),





]
