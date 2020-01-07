from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db.models import Q
import json
from . import models
from .models import *
from . import forms
import hashlib
import random


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

'''
def search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/search.html')
'''

def search_result(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/search_result.html')
'''
def state(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/state.html')
'''

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

'''
def arrange(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'CS_app/arrange.html')
'''
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
                    return redirect('/search/')
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
        "08:00-09:30": 1, "10:00-11:30": 2, "12:00-13:30": 3,
        "14:00-15:30": 4, "16:00-17:30": 5, "18:00-19:30": 6,
        "19:40-21:10": 7, "08:00-10:30": 8, "14:00-16:30": 9, "18:00-21:00": 10
    }
    return period_num[x]

def Num2Period(x):
    num_period = {
        1: "08:00-09:30", 2: "10:00-11:30", 3: "12:00-13:30",
        4: "14:00-15:30", 5: "16:00-17:30", 6: "18:00-19:30",
        7: "19:40-21:10",8 : "08:00-10:30", 9: "14:00-16:30", 10: "18:00-21:00"
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

def Status2Num(x):
    status_num = {"未通过": 1, "申请中": 2, "尚未排课": 3, "已排课": 4}
    return status_num[x]

def Num2Status(x):
    status_name = {1: "未通过", 2: "申请中", 3: "尚未排课", 4: "已排课"}
    return status_name[x]

def TimeDivide(x): # x in [1 - 5]
    Num = [
        [1, 0], [1, 0],
        [0, 1], [2, 0], [1, 1]
    ]
    return Num[int(x)-1]

src = []
Room_List = []
room_num = 0
init_flag = 1

### STUDENT ###

def search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    if request.method != 'POST':
        return render(request, 'CS_app/search.html', locals())

    d = request.POST.get('date') # list
    t = request.POST.get('time')
    p = request.POST.get('place')
    #print(d, t, p) #DEBUG

    tmp = Schedule.objects.select_related("room", "time1", "time2", "course__tid1").all()

    if d != '':
        day = GET_WEEKDAY(d)
        tmp = tmp.filter(Q(time1__weekday = day) | Q(time2__weekday = day))
    if t != '所有' and t != '':
        per = Period2Num(t)
        tmp = tmp.filter(Q(time1__period = per) | Q(time2__period = per))
    if p != '所有' and p != '':
        tmp = tmp.filter(room__rname = p)

    #print('tmp = ', tmp)

    # ["程序设计",4,40,"专业必修","赵鑫","星期一 8:00-9:30|星期四 16:00-17:30","公教2楼2232"],
    ret = []
    for sch in tmp:
        obj = sch.course
        t = DayName(sch.time1.weekday) + ' ' + Num2Period(sch.time1.period)
        r = sch.room.rname + ' ' + str(sch.room.room_id)
        if sch.time2 != None:
            t = t + ' | ' + DayName(sch.time2.weekday) + ' ' + Num2Period(sch.time2.period)
        ret.append([
            obj.cname, obj.credit, obj.num, Type2Name(obj.is_compulsory), obj.tid1.tname, t, r
        ])


    qwq = json.dumps(ret)# + json.dumps(ret[0])
    #ERROR_LIST(qwq)

    return render(request, 'CS_app/search_result.html', {
        'res': qwq,
    })
    #return HttpResponse('get')

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
    for obj in tmp:
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

'''
### Teacher ###
# Query status
def state(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    #if request.method != 'POST':
    #    return render(request, 'CS_app/index_teacher.html', locals()) # Teacher

    tmp = Apply.objects.select_related("tid1").filter(tid1__tid=int(request.session.get('user_name')))
    qwq = Schedule.objects.select_related("course__tid1", "time1", "time2", "room").filter(course__tid1__tid=int(request.session.get('user_name')))


    ret = []
    for sch in qwq:
        obj = sch.course
        tea = obj.tid1
        t = DayName(sch.time1.weekday) + ' ' + Num2Period(sch.time1.period)
        r = sch.room.rname + ' ' + str(sch.room.room_id)
        if sch.time2 != None:
            t = t + ' | ' + DayName(sch.time2.weekday) + ' ' + Num2Period(sch.time2.period)
        ret.append([obj.cname, obj.credit, obj.num, Type2Name(obj.is_compulsory), tea.tname, Num2Status(obj.status), t, r])

    for obj in tmp:
        if obj.status == 4:
            continue

        tea = obj.tid1

        t = '-'
        r = '-'
        #ret.append({
        #    'cname': obj.cname,
        #    'credit': obj.credit,
        #    'num': obj.num,
        #    'ctype': obj.is_compulsory,
        #    'tname': tea.tname,
        #    'status': obj.status,
        #    'time': t,
        #    'room': r
        #})
        ret.append([obj.cname, obj.credit, obj.num, Type2Name(obj.is_compulsory), tea.tname, Num2Status(obj.status), t, r])


    return render(request, 'CS_app/state.html', {'res': json.dumps(ret), })


## Admin
def arrange(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    #if request.method != 'POST':
    #    return render(request, 'CS_app/index_teacher.html', locals()) # Teacher

    tmp = Apply.objects.select_related("tid1").all()
    qwq = Schedule.objects.select_related("course__tid1", "time1", "time2", "room").all()


    ret = []
    for sch in qwq:
        obj = sch.course
        tea = obj.tid1
        t = DayName(sch.time1.weekday) + ' ' + Num2Period(sch.time1.period)
        r = sch.room.rname + ' ' + str(sch.room.room_id)
        if sch.time2 != None:
            t = t + ' | ' + DayName(sch.time2.weekday) + ' ' + Num2Period(sch.time2.period)
        ret.append([obj.cname, obj.credit, obj.num, Type2Name(obj.is_compulsory), tea.tname, Num2Status(obj.status), t, r])

    for obj in tmp:
        if obj.status == 4:
            continue

        tea = obj.tid1

        t = '-'
        r = '-'
        #ret.append({
        #    'cname': obj.cname,
        #    'credit': obj.credit,
        #    'num': obj.num,
        #    'ctype': obj.is_compulsory,
        #    'tname': tea.tname,
        #    'status': obj.status,
        #    'time': t,
        #    'room': r
        #})
        ret.append([obj.cname, obj.credit, obj.num, Type2Name(obj.is_compulsory), tea.tname, Num2Status(obj.status), t, r])


    return render(request, 'CS_app/arrange.html', {'res': json.dumps(ret), })




def TimeID(day, period):
    return day * 10 + period + 1

def GetTime(srci, L, last):
    ConflictMatrix = [ [0],
        [1, 8],
        [2, 8],
        [3],
        [4, 9],
        [5, 9],
        [6, 10],
        [7, 10],
        [8, 1, 2],
        [9, 4, 5],
        [10, 6, 7]
    ]

    iter1 = list(range(5)) # random
    random.shuffle(iter1)
    if last != 10:
        iter1.remove(last)
        if last != 4:
            iter1.remove((last + 1) % 7)
            #iter1.append((last+1)%7)
        if last != 0:
            iter1.remove((last+6)%7)
            #iter1.append((last+6)%7)
    random.shuffle(L)
    for i in iter1:
        for j in L:
            if srci[TimeID(i, j)] == True:
                vec = ConflictMatrix[j]
                for k in vec:
                    srci[TimeID(i, k)] = False
                    if k>=8:
                        srci[1] -= 1
                    else:
                        srci[0] -= 1
                #print(TimeID(i, j)-1)
                return TimeID(i, j)-1
    return -1

# [3] : [8, 9, 10]
def CheckRoom(room, num2, num3, srci):
    if srci[0] >= num2+num3*2 and srci[1] >= num3:
        #print(room.rid, ' ', str(num2) + ' ' + str(num3), ' ', srci[0], ' ', srci[1], ' ', num2+num3*2)
        flag = 10
        ret = []
        for i in range(num3):
            tmp = GetTime(srci, [8,9,10], flag)
            ret.append(tmp)
            if tmp!=-1:
                flag = (tmp-1)//10
        #print('tmp' +str(ret))
        for i in range(num2):
            tmp = GetTime(srci, [x for x in range(1,8)], flag)
            ret.append(tmp)
            if tmp!=-1:
                flag = (tmp-1)//10
        #print(ret)
        #print(room.rid, ' ', str(num2) + ' ' + str(num3), ' ', srci[0], ' ', srci[1], ' ', num2 + num3 * 2)
        ret = sorted(ret, reverse=False)
        return ret
    return [-1]


def Init_Room():
    global Room_List, room_num, src
    ConflictMatrix = [[0], [1, 8], [2, 8], [3],
                      [4, 9], [5, 9], [6, 10], [7, 10],
                      [8, 1, 2], [9, 4, 5], [10, 6, 7] ]
    Sch = Schedule.objects.select_related("time1", "time2", "room")
    Room_List = list(Room.objects.all())
    room_num = len(Room_List)

    Room_List = sorted(Room_List, key=lambda x: x.capacity, reverse=False)
    mp = {}
    src = [[7 * 5, 3 * 5] + [True for y in range(70)] for x in range(room_num)]

    for i,x in enumerate(Room_List):
        mp[x.rid] = i

    for sc in Sch:
        i = mp[sc.room.rid]
        x, y = sc.time1.weekday, sc.time1.period
        #pos = TimeID(x, y)
        vec = ConflictMatrix[y]
        for k in vec:
            src[i][TimeID(x, k)] = False
            if k >= 8:
                src[i][1] -= 1
            else:
                src[i][0] -= 1
        if sc.time2 == None:
            continue
        x, y = sc.time2.weekday, sc.time2.period
        #pos = TimeID(x, y)
        vec = ConflictMatrix[y]
        for k in vec:
            src[i][TimeID(x, k)] = False
            if k >= 8:
                src[i][1] -= 1
            else:
                src[i][0] -= 1



# scheduling 尚未排课->开课成功
def schedule(app):
    global Room_List, room_num, src, init_flag
    if (init_flag):
        Init_Room()
        init_flag = 0

    [num2, num3] = TimeDivide(app.credit)
    Flag = 1

    for (srci, room) in zip(src, Room_List):  # find a room
        if room.capacity < app.num:
            continue

        res = CheckRoom(room, num2, num3, srci)  # time period
        if res[0] != -1:  # Find
            sch = Schedule()
            sch.course = app
            sch.room = room
            sch.time1 = Time.objects.get(weekday=(res[0]-1)//10, period=(res[0]-1)%10+1)
            if len(res)==1:
                sch.time2 = None
            else:
                sch.time2 = Time.objects.get(weekday=(res[1]-1)//10, period=(res[1]-1)%10+1)
            sch.save()

            Flag = 0
            break
    # print('app end', appid)
    if Flag != 1:
        app.status = 4
        app.save()
        return 1 # successful
    else:
        return 0 # fail


# Teacher Apply
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

    app.status = 2
    app.save() #TEMP
    # ERROR_LIST([app.aid, app.status, app.cname, app.credit, app.is_compulsory, app.num])
    #schedule(app) # ???
    #return HttpResponse('申请提交成功！')
    #return HttpResponse(app.cname + str(app.credit) + app.is_compulsory +app.tid1.tname+str(app.num))
    return redirect('/opening_result/')

### Administrator

# reply 申请中->尚未排课 / 拒绝
def apply(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    tmp = Apply.objects.select_related("tid1").filter(status=2)
    #tmplist = list(tmp)
    #print(tmplist)

    # print(request.method) # GET
    # if request.method != 'POST': ## init
    #     return render(request, 'CS_app/apply.html', {'res': json.dumps(ret), })

    R = request.GET.get('row')
    F = request.GET.get('flag') # 0 pass

    #print(R, type(R)) str / None
    #print(F, type(F))

    # if search
    #
    #

    if R == None or F == None:  ## init
        pass
    else:
        # Pass or Not
        app = tmp.get(aid=int(R)) # aid:int
        if F == '0': # pass
            schedule(app)
        else:
            app.status = 1
            app.save()
            pass

    #  ["数据结构",2,100,"专业必修","张孝"],
    ret = []
    for obj in tmp:
        tea = obj.tid1
        ret.append([obj.aid, obj.cname, obj.credit, obj.num, Type2Name(obj.is_compulsory), tea.tname])


    return render(request, 'CS_app/apply.html', {'res': json.dumps(ret), })



# Test
def get_post(request):
    if request.method == 'GET':
        R = request.GET.get('row')
        F = request.GET.get('flag')
        print(R)
        print(F)
    return render(request, 'CS_app/index_student.html')

# 原则上
# 不排周末
# 小教室优先
# 高学分优先
# 尽量同一教室
def init_schedule(room_num, Room_List, Apply_List):

    Ti = Time.objects.all()

    Room_List = sorted(Room_List, key=lambda x: x.capacity, reverse=False)
    Apply_List = sorted(Apply_List, key=lambda x: x.credit, reverse=True)

   # Ti = Time.objects().all()

    # WeekDays
    global src
    src = [[7 * 5, 3 * 5] + [True for y in range(70)] for x in range(room_num)]

    # ans = {}
    # k1, k2 = 0, 0
    # [n1, n2] = [0, 0]
    # appid = 0
    for app in Apply_List:
        if app.status == 3:
            [num2, num3] = TimeDivide(app.credit)
            # [n1, n2] = [n1+num2, n2+num3]
            Flag = 1

            #appid+=1
            # print('app begin', appid)
            for (srci,room) in zip(src, Room_List): # find a room
                if room.capacity < app.num:
                    continue

                res = CheckRoom(room, num2, num3, srci) # time period
                if res[0] != -1: # Find
                    #DEBUG
                    # if res[0] <= 0 or res[0] > 70 or ans.get(str(room.rid) + ',' + str(res[0])):
                    #     ERROR_LIST('conflict')
                    #     return
                    # else:
                    #     ans[str(room.rid) + ',' + str(res[0])] = 1
                    #     if (res[0]-1)%10>6:
                    #         k2 += 1
                    #     else:
                    #         k1 += 1
                    # if len(res) > 1:
                    #     if res[1] <= 0 or res[1] > 70 or ans.get(str(room.rid) + ',' + str(res[1])):
                    #         ERROR_LIST('conflict')
                    #         return
                    #     else:
                    #         ans[str(room.rid) + ',' + str(res[1])] = 1
                    #         if (res[1] - 1) % 10 > 6:
                    #             k2 += 1
                    #         else:
                    #             k1 += 1

                    #n0 = []
                    #n1 = []
                    #for x in src:
                    #    n0.append(x[0])
                    #    n1.append(x[1])
                    #print("n0: ", n0, '\n', "n1: ", n1)
                    sch = Schedule()
                    sch.course = app
                    sch.room = room
                    sch.time1 = Ti.get(weekday=(res[0]-1)//10, period=(res[0]-1)%10+1)
                    if len(res)==1:
                       sch.time2 = None
                    else:
                        if res[1]<=0 or res[1]>70:
                            ERROR_LIST(res)
                        sch.time2 = Ti.get(weekday=(res[1]-1)//10, period=(res[1]-1)%10+1)
                    sch.save()

                    Flag = 0
                    break
            # print('app end', appid)
            if Flag != 1:
                app.status = 4
                app.save()

    # WeekEnds NoNoNo
    for i in range(room_num):
        src[i][0] += 7 * 2
        src[i][1] += 3 * 2

    for app in Apply_List:
        if app.status == 3:
            [num2, num3] = TimeDivide(app.credit)
            Flag = 1

            for (srci,room) in zip(src, Room_List): # find a room
                if room.capacity < app.num:
                    continue

                res = CheckRoom(room, num2, num3, srci)
                if res[0] != -1: # Find

                    sch = Schedule()
                    sch.course = app
                    sch.room = room
                    sch.time1 = Ti.get(weekday=(res[0] - 1) // 10, period=(res[0] - 1) % 10 + 1)
                    if len(res) == 1:
                        sch.time2 = None
                    else:
                        sch.time2 = Ti.get(weekday=(res[1] - 1) // 10, period=(res[1] - 1) % 10 + 1)
                    sch.save()

                    Flag = 0
                    break

            if Flag != 1:
                app.status = 4
                app.save()
            else:
                ERROR_LIST("Lack of Room")
                break
    ### check

def build_small_test_case():
    tmp = Apply.objects.filter(aid__gte=1996, aid__lt=1999)
    for app in tmp:
        schedule(app)
    for app in tmp:
        print(app.status)

def init_data(test_small_case = 0):
    global Room_List, room_num
    tea_num, Teacher_List = 0, {}
    time_num = 0
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
        Teacher_List[tid] = Tea
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
        app.tid1 = Teacher_List[tid]#Teacher.objects.get(tid=tid)
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

    if test_small_case:
        build_small_test_case()
    else:
        init_schedule( room_num, Room_List, Apply_List )
    print('finished ..')