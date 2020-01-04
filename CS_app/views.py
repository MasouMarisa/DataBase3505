from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import hashlib
# Create your views here.

def hash_code(s, salt='CS_project'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/index.html')

def search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/search.html')

def search_result(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/search_result.html')

def state(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/state.html')

def opening(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/opening.html')

def opening_result(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/opening_result.html')

def arrange(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/arrange.html')

def apply(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/apply.html')

def index_student(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/index_student.html')

def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.User.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'CS_app/login.html', locals())
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                if user.identity == 'student':
                    return redirect('/index_student/')
                if user.identity == 'teacher':
                    return redirect('/state/')
                if user.identity == 'administrator':
                    return redirect('/arrange/')
            else:
                message = '密码不正确！'
                return render(request, 'CS_app/login.html', locals())
        else:
            return render(request, 'CS_app/login.html', locals() )
        
    login_form = forms.UserForm()       #后续只需要{{login_form}}即可创建表单
    return render(request, 'CS_app/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            identity = register_form.cleaned_data.get('identity')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'CS_app/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'CS_app/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'CS_app/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.identity = identity
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, 'CS_app/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'CS_app/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")