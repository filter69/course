import hashlib
import random
import string

import traceback
import uuid


from captcha.image import ImageCaptcha
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, HttpResponse, redirect

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.contrib.auth import settings

from user.models import TUser
# Create your views here.


def register(request):
    return render(request,'user/register.html')


def pd_name(request):
    username = request.POST.get('username')
    print(username)
    u = TUser.objects.filter(name=username)
    if u:
        return HttpResponse('用户名已存在')
    return  HttpResponse('ok')


def regist_verify(request):
    try:
        captcha = request.POST.get('captcha')
        if captcha.lower() == request.session.get('code').lower():
            username = request.POST.get('username')
            password = request.POST.get('pwd')
            password1 = request.POST.get('pwd1')
            salt = str(uuid.uuid4())  # 生成盐
            salt1 = salt.split('-')
            sha = hashlib.sha1()    #声明对象
            sha.update((salt1[0]+password).encode('utf-8'))
            password = sha.hexdigest()  # 加密
            sha = hashlib.sha1()
            sha.update((salt1[0] + password1).encode('utf-8'))
            password1 = sha.hexdigest()
            email = request.POST.get('email')
            if username == '' or password == '':
                return HttpResponse('用户名密码不能为空')
            if password == password1:
                u = TUser.objects.filter(name=username)
                if not u:
                    with transaction.atomic():
                        user = TUser(name=username, password=password,email=email,is_active=0,salt=salt1[0])
                        user.save()
                        ser = Serializer(settings.SECRET_KEY, expires_in=180)   #使用setting秘钥编码
                        id = u.values('id')[0]['id']
                        result = ser.dumps({'id': id})
                        send_mail('账号激活邮件','用户'+username+'请求激活帐号,链接为:http://127.0.0.1:8000/user/active/?token='+result.decode('utf-8'),
                                  '1242541741@qq.com',['1242541741@qq.com'])
                        return HttpResponse('注册成功')
                else:
                    return HttpResponse('用户名已存在')
            else:
                return HttpResponse('密码不一致')
        else:
            return HttpResponse('验证码错误')
    except:
        traceback.print_exc()
        return HttpResponse('注册失败')


def email(request):
    try:
        username = request.GET.get('username')
        u = TUser.objects.filter(name=username)
        id = u.values('id')[0]['id']
        ser = Serializer(settings.SECRET_KEY, expires_in=180)  #使用秘钥编码
        result = ser.dumps({'id': id})
        send_mail('账号激活邮件','用户'+username+'请求激活帐号,链接为:http://127.0.0.1:8000/user/active/?token='+result.decode('utf-8'),
                '1242541741@qq.com',['1242541741@qq.com'])
        return HttpResponse('邮件发送成功')
    except:
        traceback.print_exc()
        return HttpResponse('邮件发送失败')

#邮件激活
def active(request):
    try:
        token = request.GET.get('token')
        ser = Serializer(settings.SECRET_KEY, expires_in=180)  #使用setting秘钥解码
        id = ser.loads(token).get('id')
        user = TUser.objects.get(pk=id)
        user.is_active = True
        user.save()
        return  HttpResponse('激活成功')
    except:
        return HttpResponse('激活失败')


def login(request):
    username = request.COOKIES.get('username')
    password = request.COOKIES.get('password')
    if username!=None and password!=None:
        username = username.encode('latin-1').decode('utf-8')
        password = password.encode('latin-1').decode('utf-8')
        res = TUser.objects.filter(name=username)
        try:
            if res:
                if res[0].is_active:
                    data = res.values('password','salt')
                    sha = hashlib.sha1()   #声明sha1()对象
                    sha.update((data[0]['salt'] + password).encode('utf-8'))
                    password = sha.hexdigest()      #密码加密
                    if password == data[0]['password']:
                        request.session['is_login'] = True  #添加登录状态
                        request.session['username'] = username  #添加登录yonghuming 状态
                        return redirect('courseapp:home')
                #     return render(request, 'user/login.html')
                # return render(request,'user/login.html')
            return render(request,'user/login.html')
        except:
            return render(request, 'user/login.html')
    else:
        return render(request, 'user/login.html')



def login_verify(request):
    username = request.POST.get('username')
    password = request.POST.get('pwd')
    password1 = password
    print(password,type(password))
    num = request.POST.get('num')
    if username=='' or password=='':
        return HttpResponse('账号或密码不能为空')
    u = TUser.objects.filter(name=username)
    if u:
        if u[0].is_active:
            sha = hashlib.sha1()  #声明sha1对象
            sha.update((u[0].salt + password).encode())
            password2 = sha.hexdigest()
            if password2 != u[0].password:
                return  HttpResponse('账号或密码错误')
            request.session['is_login'] = True
            request.session['username'] = username
            resp = HttpResponse('登录成功')
            if num:
                username = username.encode('utf-8').decode('latin-1')
                pwd = password1.encode('utf-8').decode('latin-1')
                resp.set_cookie('username', username, max_age=3600*24*7)
                resp.set_cookie('password', pwd, max_age=3600*24*7)
            return  resp
        else:
            print(111)
            return HttpResponse("账号未激活")
    return HttpResponse('账号或密码错误')


def get_captcha(request):
    image = ImageCaptcha()
    code = random.sample(string.ascii_letters+string.digits,4)
    code = ''.join(code)
    data = image.generate(code)
    request.session['code'] = code
    print(code)
    return HttpResponse(data,'image/png')


#渲染忘记密码页面
def forget(request):
    return render(request,'user/forget_pwd.html')


#忘记密码提交逻辑
def forget_verify(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    print(name)
    print(email)
    u = TUser.objects.filter(name=name, email=email)
    if u:
        request.session['is_forget'] = True
        return  HttpResponse('ok!'+name)
    return HttpResponse('error')


#渲染重置密码页面
def reset_pwd(request):
    return render(request,'user/reset_pwd.html')


def reset_pwd_verify(request):
    pwd = request.POST.get('')
    pwd1 = request.POST.get('')
    name = request.GET.get('name')
    if pwd == pwd1:
        salt = str(uuid.uuid4())
        salt = salt.split('-')
        sha = hashlib.sha1
        sha.update((salt[0]+pwd).encode())
        pwd = sha.hexdigest()
        user = TUser.objects.filter(name=name)

    return HttpResponse('密码不一致')


#退出
def quit(request):
    request.session.flush()
    res  = redirect('user:login')
    res.delete_cookie("username")
    res.delete_cookie("password")
    return res


def quite(request):
    return render(request,'user/logout.html')