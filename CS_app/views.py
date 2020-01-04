from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db.models import Q
from . import models
from .models import *
from . import forms
import hashlib

import datetime

# Create your views here.

### URL ###

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

'''
def opening(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/opening.html')
'''

def opening_result(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/opening_result.html')

def arrange(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/arrange.html')
'''
def apply(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/apply.html')
'''
def index_student(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/index_student.html')


### FORM ###
### LOG & REGISTER ###

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
                user = User.objects.get(name=username)
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
                same_name_user = User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'CS_app/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'CS_app/register.html', locals())

                new_user = User()
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


### FORMAT ###
def ERROR_LIST(l):
    print("****** \n\n\n\n\n\n\n")
    print(l)
    print("\n\n\n\n\n\n\n******")

def GET_WEEKDAY(d): # YYYT-MM-DD -> Day Number [0..6]
    [YEAR,MONTH,DAY] = list(map(int, d.split('-') ))
    return datetime.datetime(YEAR, MONTH, DAY).weekday()

def DayName(x):
    Name = ["一", "二", "三", "四", "五", "六", "日"]
    return "星期" + Name[x]

def Period2Num(x):
    period_num = {
        "8:00-9:30": 1, "10:00-11:30": 2, "12:00-13:30": 3,
        "14:00-15:30": 4, "16:00-17:30": 5, "18:00-19:30": 6,
        "19:40-21:10": 7, "8:00-10:30": 8, "14:00-16:30": 9, "18:00-21:00": 10
    }
    return period_num[x]

def Num2Period(x):
    num_period = {
        1: "8:00-9:30", 2: "10:00-11:30", 3: "12:00-13:30",
        4: "14:00-15:30", 5: "16:00-17:30", 6: "18:00-19:30",
        7: "19:40-21:10",8 : "8:00-10:30", 9: "14:00-16:30", 10: "18:00-21:00"
    }
    return num_period[x]

def Type2Name(x):
    Name = {
        'COMPULSORY': '专业必修',
        'UNCOMPULSORY': "专业选修",
        'UNKNOWN': "未知",
    }
    return Name[x]

def Name2Type(x):
    Type = {'专业必修': 'COMPULSORY', "专业选修": 'UNCOMPULSORY', "未知": 'UNKNOWN'}
    return Type[x]

### STUDENT ###
'''
def index_student(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    if request.method != 'POST':
        squery_form = forms.SQueryForm()
        return render(request, 'CS_app/index_student.html', locals())

    squery_form = forms.SQueryForm(request.POST)

    if not squery_form.is_valid():
        return render(request, 'CS_app/index_student.html', locals())



    d = squery_form.cleaned_data.get('day') # item
    t = squery_form.cleaned_data.get('time')
    p = squery_form.cleaned_data.get('place')

    #d = request.POST.getlist('Sdate') # list
    #t = request.POST.getlist('Stime')
    #p = request.POST.getlist('Splace')
    #print(d, t, p) #DEBUG

    period_num = {
        "8:00-9:30": 1, "10:00-11:30": 2, "12:00-13:30": 3,
        "14:00-15:30": 4, "16:00-17:30": 5, "18:00-19:30": 6,
        "19:40-21:10": 7, "8:00-10:30": 8, "14:00-16:30": 9, "18:00-21:00": 10
    }

    tmp = Schedule.objects.filter(students__name=request.session.get('user_name'))

    if d != '':
        day = GET_WEEKDAY(d)
        tmp = tmp.filter(rt__time__weekday = day)
    if t != '所有' and t != '':
        tmp = tmp.filter(rt__time__period = period_num)
    if p != '所有' and p != '':
        tmp = tmp.filter(rt__room__rname = p)

    print('tmp = ', tmp)

    #return render(request, 'CS_app/query_student.html', {'res': tmp})
    return HttpResponse('get')
'''
'''
### Teacher & Admin & Student ###
# Query All
def query(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    if request.method != 'POST':
        query_form = forms.QueryForm()
        return render(request, 'CS_app/.html', locals()) # Teacher or Admin

    query_form = forms.QueryForm(request.POST)

    if not query_form.is_valid():
        return render(request, 'CS_app/.html', locals())

    d = query_form.cleaned_data.get('day') # item
    t = query_form.cleaned_data.get('time')
    p = query_form.cleaned_data.get('place')

    #d = request.POST.getlist('day')
    #t = request.POST.getlist('time')
    #p = request.POST.getlist('place')
    # print(d, t, p)

    #tmp = Schedule.objects.all()
    #if d != '':
    #    day = GET_WEEKDAY(d[0])
    #    tmp = tmp.filter(rt__time__weekday=day)
    #if t != '所有' and t != '':
    #    tmp = tmp.filter(rt__time__period=period_num[t])
    #if p != '所有' and p != '':
    #    tmp = tmp.filter(rt__room__rname=p)

    tmp = Apply.objects.all()
    ret = []
    for obj in tmp.objects.all():
        sch = obj.schedule_set.all()[0] # only
        tea = obj.tid1

        t = '-'
        r = '-'
        if sch.exists():
            tmp = sch.rt.all() # 1-2 rt
            t = DayName(tmp[0].time.weekday) + ' ' + Num2Period(tmp[0].time.period)
            r = tmp[0].room.rname + ' ' + str(tmp[0].room.room_id)
            if len(tmp) > 1:
                t = t + ' | ' + DayName(tmp[1].time.weekday) + ' ' + Num2Period(tmp[1].time.period)
        ret.append({
            'cname': obj.cname,
            'credit': obj.credit,
            'num': obj.num,
            'ctype': obj.is_compulsory
            'tname': tea.tname,
            'status':  obj.status,
            'time':  t,
            'room': r
        })

    return render(request, 'CS_app/query.html', {'': ret})
    #return HttpResponse('get')


### Teacher ###
# Query status
def tquery(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    if request.method != 'POST':
        tquery_form = forms.TQueryForm()
        return render(request, 'CS_app/index_teacher.html', locals()) # Teacher

    tquery_form = forms.TQueryForm(request.POST)

    if not tquery_form.is_valid():
        return render(request, 'CS_app/index_teacher.html', locals())


    status_num = {"未通过":1, "申请中":2, "尚未排课":3, "已排课":4 }
    sta = tquery_form.cleaned_data.get('status')
    tmp = Apply.objects.filter(tid1__tname = request.session.get('user_name'))#.filter(tid2__tname = request.session.get('user_name'))

    if sta:
        for st in sta:
            tmp = tmp.filter(status = status_num[st])
    return render(request, 'CS_app/query_teacher.html', locals())
'''

# Apply
def opening(request): ## insert
    if not request.session.get('is_login', None):
        return redirect('/login/')

    if request.method != 'POST':
        return render(request, 'CS_app/opening.html', locals())

    #t = datetime.datetime.now()

    try:
        # ! tid -> int
        app_tea = Teacher.objects.get(tid=int(request.session.get('user_name')))

        name_ = request.POST.get('name')
        n = request.POST.get('num')
        #ERROR_LIST(name_ + n)
        if name_ == "" or n == "":
            ERROR_LIST("empty")
            return render(request, 'CS_app/opening.html', locals())

        app = Apply()
        #app.aid = str(t.year)+str(t.month)+str(t.day)+str(t.hour)+str(t.minute)+str(t.second)
        app.cname = name_

        app.credit = int(request.POST.get('credit'))
        app.is_compulsory = Name2Type(request.POST.get('is_compulsory'))
        #app.target = tapply_form.cleaned_data.get('target')
        app.cdepart = app_tea.tdepart
        app.tid1 = app_tea
        #tmp = tapply_form.cleaned_data.get('teacher')
        #if tmp != '':
        #    app.tid2 = Teacher.objects.get(tname=tmp)
        #else:
        #    app.tid2 = None
        #app.tid2 = request.POST.get('teacher')
        app.num = int(n)
    except:
        # ERROR_LIST("23333333")
        return render(request, 'CS_app/opening.html', locals())

    #app.save() #TEMP
    #return HttpResponse('申请提交成功！')
    #return HttpResponse(app.cname + str(app.credit) + app.is_compulsory +app.tid1.tname+str(app.num))
    return redirect('/opening_result/')


### Administrator

# reply 申请中->尚未排课 / 拒绝
def apply(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    tmp = Apply.objects.filter(status=2)
    #  ["数据结构",2,100,"专业必修","张孝"],
    ret = []
    for obj in tmp:
        tea = obj.tid1
        ret.append([obj.cname, obj.credit, obj.num, obj.is_compulsory, tea.tname])

    if request.method != 'POST': ## init
        return render(request, 'CS_app/apply.html', {'ret': ret})

    v1 = request.POST.get('Y')
    v2 = request.POST.get('N')

    ERROR_LIST([v1,v2])



    # if search
    #
    #

    #
    return render(request, 'CS_app/apply.html', {'ret': ret})





'''
# scheduling 尚未排课->开课成功
def aschedule(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    if request.method != 'POST':
        schedule_form = forms.ScheduleForm()
        return render(request, 'CS_app/index_admin.html', locals())  # Teacher

    schedule_form = forms.ScheduleForm(request.POST)

    if not schedule_form.is_valid():
        return render(request, 'CS_app/index_admin.html', locals())

    d = schedule_form.cleaned_data.get('day')  # item
    t = schedule_form.cleaned_data.get('time')
    p = schedule_form.cleaned_data.get('place')

    tid = DAY[d]*10 + TIME[t]

    tmp = R_T.objects.filter(room_name=p, time__tid=tid)
'''

















# Test
def get_post(request):
    print("INEL YES")
    if request.method == 'POST':
        print('AMD YES')

# 原则上
# 不排周末
# 小教室优先
# 高学分优先
# 尽量同一教室
def init_schedule(tea_num, Teacher_List, time_num, Time_List,
        room_num, Room_List, apply_num, Apply_List):

    sorted(Room_List, key=lambda x: x.capacity, reverse=False)
    src = [[7, 3]] * room_num

    pass

def init_data():
    tea_num, Teacher_List = 0, []
    time_num, Time_List = 0, []
    room_num, Room_List = 0, []
    apply_num, Apply_List = 0, []

    # Teacher
    f = open('../data/teacher.csv', mode='r')
    for s in f:
        [tid, tname, tdepart] = s.strip('\n').split(',')
        Tea = Teacher()
        Tea.tid = tid
        Tea.tname = tname
        Tea.tdepart = tdepart
        Tea.save()
        tea_num += 1
        Teacher_List.append(Tea)
    f.close()

    # User id,name,password,email,identity
    f = open('../data/user.csv', mode='r')
    for s in f:
        [uid, name, password, email, identity] = s.strip('\n').split(',')
        usr = User()
        usr.name = name
        usr.password = password
        usr.email = email
        usr.identity = identity
        usr.save()
    f.close()

    # Time
    f = open('../data/time.csv', mode='r')
    for s in f:
        [tmid, weekday, period] = s.strip('\n').split(',')
        t = Time()
        t.tmid = tmid
        t.weekday = int(weekday)
        t.period = int(period)
        t.save()
        time_num += 1
        Time_List.append(t)
    f.close()

    # Room 1,明德新闻楼,2,0206,23
    f = open('../data/room.csv', mode='r', encoding='utf-8')
    for s in f:
        [rid, rname, floor, room_id, capacity] = s.strip('\n').split(',')
        rm = Room()
        rm.rid = rid
        rm.rname = rname
        rm.floor = floor
        rm.room_id = room_id
        rm.capacity = int(capacity)
        rm.save()
        room_num += 1
        Room_List.append(rm)
    f.close()

    # Apply 1,2013100000,程序设计,COMPULSORY,2,20,3 cdepart
    f = open('../data/apply.csv', mode='r')
    for s in f:
        [aid, tid, cname, is_compulsory, credit, num, status] = s.strip('\n').split(',')
        app = Apply()
        app.aid = aid
        app.tid1 = Teacher.objects.get(tid=tid)
        app.tid2 = None
        app.cname = cname
        app.is_compulsory = is_compulsory
        app.credit = credit
        app.num = int(num)
        app.status = int(status)
        app.cdepart = app.tid1.tdepart
        app.save()
        apply_num += 1
        Apply_List.append(app)
    f.close()

    print('load into db .. ', tea_num, time_num, room_num, apply_num)

    init_schedule(tea_num, Teacher_List,
        time_num, Time_List,
        room_num, Room_List,
        apply_num, Apply_List
    )
    print('finished ..')