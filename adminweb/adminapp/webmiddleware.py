# -*- coding: utf-8 -*-
# @Time    : 2022/3/28 14:59
# @Author  : huni
# @Email   : zcshiyonghao@163.com
# @File    : webmiddleware.py
# @Software: PyCharm
from django.shortcuts import redirect
from django.urls import reverse
import re


class WebMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        path = request.path

        # 判断管理后台是否登录
        # 定义允许后台不登陆也可以直接访问的URL地址列表
        url_list = ['/web/login', '/web/dologin', '/web/logout', '/web/verify', '/web/register', '/web/doregister']
        # 判断当前URL是否以url开头  并且不在url_list中
        if re.match(r'^/web', path) and path not in url_list:
            # 判断是否登录
            if 'adminuser' not in request.session:
                # 没有登录就重定向到登陆的页面
                return redirect(reverse('login'))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
