from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator

from datetime import datetime
import time
from ..models import Site_Cookie


def select_site(request, page = 1,per_page = 10):
    cookie_ob = Site_Cookie.objects.all()


    # 获取并判断关键字搜索条件
    mywhere = []  # 条件维持
    kw = request.GET.get('keyword', None)
    if kw:
        cookie_ob = cookie_ob.filter(Q(username__contains = kw) | Q(sitename__contains = kw))
        mywhere.append('keyword=' + kw)

    # 判断状态搜索
    status = request.GET.get('status', '')
    if status != '':
        cookie_ob = cookie_ob.filter(status = status)
        mywhere.append('status=' + status)
    else:
        cookie_ob = cookie_ob.filter(status = 1)

    # 分页处理
    page = int(page)
    every_page = Paginator(cookie_ob, per_page)  # 每10条数据分页
    max_page = every_page.num_pages  # 最大页数

    # 判断当前页是否越界
    if page < 1:
        page = 1
    elif page > max_page:
        page = max_page

    # 获取当前页数据
    user_info = every_page.page(page)

    # 获取页码列表信息
    page_list = every_page.page_range

    # ulist = p.page(page)
    context = {'user_info': user_info, 'page': page, 'page_list': page_list, 'mywhere': mywhere,'per_page':per_page}
    return render(request, 'homeadmin/op_cookie/select.html', context)


def get_cookie(request, siteid):
    try:
        cookie_ob = Site_Cookie.objects.get(id = siteid)
        cookie_json = {
            'msg': 'ok',
            'data': {
                'sitename': cookie_ob.sitename,
                'siteaddress': cookie_ob.siteaddress,
                'username': cookie_ob.username,
                'site_cookie': cookie_ob.site_cookie,
                'status': cookie_ob.status,
                'create_at': cookie_ob.create_at,
                'update_at': cookie_ob.update_at,
            }
        }
        return JsonResponse(cookie_json)
    except Exception as e:
        return JsonResponse({
            'msg': 'error',
            'data': {'e': e
                     }
        })


def add_cookie(request):
    return render(request, 'homeadmin/op_cookie/add_cookie.html')


def insert_cookie(request):
    try:
        ob = Site_Cookie()
        ob.sitename = request.POST.get('sitename')
        ob.siteaddress = request.POST.get('siteaddress')
        ob.username = request.POST.get('username')
        ob.site_cookie = request.POST.get('site_cookie')
        # 将当前员工的密码做md5处理
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
        context = {'info': '添加成功'}
    except Exception as e:
        print(e)
        context = {'info': '添加失败'}

    return render(request, 'homeadmin/op_cookie/add_cookie.html', context)


def del_cookie(request, siteid):
    try:
        ob = Site_Cookie.objects.get(id = siteid)
        ob.status = 9
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info': '删除成功'}
    except Exception as e:
        print(e)
        context = {'info': '删除失败'}

    return render(request, 'homeadmin/info.html', context)

def batch_del_cookie(request):
    try:
        siteidlist = request.POST.getlist('vals')
        if siteidlist != []:
            for siteid in siteidlist:
                ob = Site_Cookie.objects.get(id = siteid)
                ob.status = 9
                ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ob.save()
            context = {'info': '删除成功'}
        else:
            context = {'info': '删除失败'}

    except Exception as e:
        print(e)
        context = {'info': '删除失败'}

    return render(request, 'homeadmin/info.html', context)


def edit_cookie(request, siteid = 0):
    try:
        ob = Site_Cookie.objects.get(id = siteid)
        context = {'site': ob}
        return render(request, 'homeadmin/op_cookie/edit_cookie.html', context)
    except Exception as e:
        print(e)
        context = {'site': '没有找到要修改的信息'}
        return render(request, 'homeadmin/info.html', context)


def update_cookie(request, siteid = 0):
    try:
        ob = Site_Cookie.objects.get(id = siteid)
        ob.siteaddress = request.POST.get('siteaddress')
        ob.username = request.POST.get('username')
        ob.status = request.POST.get('status')
        ob.site_cookie = request.POST.get('site_cookie')
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info': "修改成功！"}
    except Exception as err:
        print(err)
        context = {'info': "修改失败！"}

    return render(request, 'homeadmin/info.html', context)
