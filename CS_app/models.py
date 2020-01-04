from django.db import models

# Create your models here.


class User(models.Model):

    IDENTITY = (
        ('administrator', "教务处"),
        ('teacher', "教师"),
        ('student', "学生"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    identity = models.CharField(max_length=64, choices=IDENTITY, default="学生")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

class Teacher(models.Model):

    tid = models.AutoField(primary_key=True)
    tname = models.CharField(max_length=128)
    tdepart = models.CharField(max_length=128)
    def __str__(self):
        return str(self.tid)

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = "教师"
'''
class Student(models.Model):

    sid = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=128)
    sdepart = models.CharField(max_length=128)
    grade = models.CharField(max_length=128)
    def __str__(self):
        return str(self.sid)

    class Meta:
        verbose_name = "学生"
        verbose_name_plural = "学生"
'''
'''
class Course(models.Model):

    COMPULSORY = (
        ('COMPULSORY', '必修'),
        ('UNCOMPULSORY', "选修"),
        ('UNKNOWN', "未知"),
    )
    cid = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=128)
    credit = models.CharField(max_length=128)
    is_compulsory = models.CharField(max_length=128,choices=COMPULSORY, default="未知")
    target = models.IntegerField()
    cdepart = models.CharField(max_length=128)
    def __str__(self):
        return str(self.cid)

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = "课程"
'''

class Room(models.Model):

    rid = models.AutoField(primary_key=True)
    rname = models.CharField(max_length=128)
    floor = models.CharField(max_length=64)
    room_id = models.CharField(max_length=64)
    capacity = models.IntegerField(null = True)
    def __str__(self):
        return str(self.rid)

    class Meta:
        verbose_name = "教室"
        verbose_name_plural = "教室"

class Time(models.Model):

    DAY = (
        (0, "周一"),
        (1, "周二"),
        (2, "周三"),
        (3, "周四"),
        (4, "周五"),
        (5, "周六"),
        (6, "周日"),
    )
    PERIOD_CHOICES = (
        (1, "8:00-9:30"),
        (2, "10:00-11:30"),
        (3, "12:00-13:30"),
        (4, "14:00-15:30"),
        (5, "16:00-17:30"),
        (6, "18:00-19:30"),
        (7, "19:40-21:10"),
        (8, "8:00-10:30"),
        (9, "14:00-16:30"),
        (10, "18:00-21:00"),
    )
    tmid = models.AutoField(primary_key=True)
    weekday = models.IntegerField(choices=DAY)
    period = models.IntegerField(choices=PERIOD_CHOICES)

    def __str__(self):
        return str(self.tmid)

    class Meta:
        verbose_name = "时间"
        verbose_name_plural = "时间"
'''
class Create_Course(models.Model):

    clid = models.AutoField(primary_key=True)
    cid = models.ForeignKey(Course, on_delete=models.CASCADE)
    tid = models.ManyToManyField(Teacher) # m Teachers
    num = models.IntegerField()
    def __str__(self):
        return str(self.clid)

    class Meta:
        verbose_name = "开课"
        verbose_name_plural = "开课"


class Teaching_class(models.Model):

    COMPULSORY = (
        ('COMPULSORY', '必修'),
        ('UNCOMPULSORY', "选修"),
        ('UNKNOWN', "未知"),
    )
    cid = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=128)
    credit = models.CharField(max_length=128)
    is_compulsory = models.CharField(max_length=128,choices=COMPULSORY, default="未知")
    target = models.IntegerField()
    cdepart = models.CharField(max_length=128)

    tid1 = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='ct1')  # 2 Teachers
    tid2 = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='ct2')
    num = models.IntegerField()

    def __str__(self):
        return str(self.cid)

    class Meta:
        verbose_name = "教学班"
        verbose_name_plural = "教学班"
'''
class Apply(models.Model):
    STATUS = (
        (1, "未通过"),
        (2, "申请中"),
        (3, "尚未排课"),
        (4, "已排课"), # -- Schedule
    )
    COMPULSORY = (
        ('COMPULSORY', '必修'),
        ('UNCOMPULSORY', "选修"),
        ('UNKNOWN', "未知"),
    )

    aid = models.AutoField(primary_key=True)
    status = models.IntegerField(choices = STATUS, default = "申请中")

    cname = models.CharField(max_length=128)
    credit = models.CharField(max_length=128)
    is_compulsory = models.CharField(max_length=128, choices=COMPULSORY, default="未知")
    #target = models.IntegerField()
    cdepart = models.CharField(max_length=128)

    tid1 = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='at1')  # 2 Teachers
    tid2 = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='at2', null=True)
    num = models.IntegerField()

    class Meta:
        verbose_name = "开课表"
        verbose_name_plural = "开课表"

class R_T(models.Model):
    rtid = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    time = models.ForeignKey(Time, on_delete=models.CASCADE)

    def __str__(self):
        return '(' + str(self.rid) + ', ' + str(self.tmid) + ')'

    class Meta:
        verbose_name = "时间-地点"
        verbose_name_plural = "时间-地点"

class Schedule(models.Model):

    course = models.ForeignKey(Apply, on_delete=models.CASCADE)
    rt = models.ManyToManyField(R_T)
    #students = models.ManyToManyField(User)  # m Student(name) -> Usr(name)

    def __str__(self):
        return str(self.clid)

    class Meta:
        verbose_name = "排课"
        verbose_name_plural = "排课"

