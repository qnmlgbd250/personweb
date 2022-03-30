from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Q

from datetime import datetime
import time
import re

from io import BytesIO

from ..models import User


# 后台管理首页
def index(request):
    return render(request, 'homeadmin/index/index.html')


# 注册
def register(request):
    return render(request, 'homeadmin/index/register.html')


# 执行注册
def doregister(request):
    try:
        # if request.POST.get('code') != request.session['verifycode']:
        #     context = {"info": '验证码错误'}
        #     return render(request, 'homeadmin/index/register.html', context)
        ob = User()
        account = request.POST.get('account','')
        phone_type = False
        email_type = False
        if re.match('^1[3-9]\d{9}$', account):
            phone_type = True
        if re.match('^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', account):
            email_type = True
        try:
            if User.objects.get(Q(username = account) | Q(email = account) | Q(phone_number = account)):
                if phone_type:
                    context = {"info": '该手机号已注册'}
                elif email_type:
                    context = {"info": '该邮箱已注册'}
                else:
                    context = {"info": '用户名被占用 请更换'}
                return render(request, 'homeadmin/index/register.html', context)
        except Exception as e:
            if str(e) in ['User matching query does not exist.']:
                # 使用正则验证
                if phone_type:
                    ob.phone_number = account
                elif email_type:
                    ob.email = account
                else:
                    ob.username = account
                import hashlib
                md5 = hashlib.md5()
                n = int(time.time())
                s = request.POST['password'] + str(n)  # 从表单中获取密码并添加干扰值
                md5.update(s.encode('utf-8'))  # 将要产生md5的子串放进去
                ob.password_hash = md5.hexdigest()  # 获取md5值
                ob.password_salt = n
                ob.status = 1
                ob.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ob.save()
                context = {'info': '注册成功'}
            else:
                context = {'info': '注册失败数据库崩溃'}
                return render(request, 'homeadmin/index/register.html', context)

    except Exception as e:
        print(e)
        context = {'info': '注册失败'}
    return render(request, 'homeadmin/index/register.html', context)


# 管理员登录表单
def login(request):
    return render(request, 'homeadmin/index/login.html')


# 执行管理员登录
def dologin(request):
    try:
        # 执行验证码的校验
        # if request.POST.get('code') != request.session['verifycode']:
        #     context = {"info": '验证码错误'}
        #     return render(request, 'homeadmin/index/login.html', context)

        # 根据登录账号获取登录者的信息
        account = request.POST.get('account')
        # 使用Q方法验证
        user = User.objects.get(Q(username = account) | Q(email = account) | Q(phone_number = account))
        # 使用正则验证
        # if re.match('^1[3-9]\d{9}$', account):
        #     user = User.objects.get(phone_number = account)
        # elif re.match('^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', account):
        #     user = User.objects.get(email = account)
        # else:
        #     user = User.objects.get(username = account)

        # 判断当前对象是不是管理员
        if user.status == 1:
            # 判断密码是否相等
            import hashlib
            md5 = hashlib.md5()

            s = request.POST['pass'] + user.password_salt  # 从表单中获取密码并添加干扰值
            md5.update(s.encode('utf-8'))  # 将要产生md5的子串放进去
            if md5.hexdigest() == user.password_hash:
                print('登录成功')
                # 登录成功后 将登陆者的信息以adminuser为key 写入到session中
                request.session['adminuser'] = user.toDict()
                # 重定向到后台管理页面
                return redirect(reverse('index'))
            else:
                context = {"info": '密码错误'}

        else:
            context = {"info": '账号无效'}

    except Exception as err:
        print(err)
        context = {"info": '登录账号不存在'}
    return render(request, 'homeadmin/index/login.html', context)


# 管理员退出
def logout(request):
    del request.session['adminuser']
    return redirect(reverse('login'))


# 输出验证码
def verify(request):
    # 引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    # 定义变量，用于画面的背景色、宽、高
    # bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242, 164, 247)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill = fill)
    # 定义验证码的备选值
    # str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '0123456789'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/AdobeArabic-Bold.otf', 35)
    # font = ImageFont.load_default().font
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, -3), rand_str[0], font = font, fill = fontcolor)
    draw.text((25, -3), rand_str[1], font = font, fill = fontcolor)
    draw.text((50, -3), rand_str[2], font = font, fill = fontcolor)
    draw.text((75, -3), rand_str[3], font = font, fill = fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
