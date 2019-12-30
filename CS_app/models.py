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

#class Teacher(models.Model):

#    tid = models.AutoField(primary_key=True)
#    tname = models.CharField(max_length=128)
#    tdepart = models.CharField(max_length=128)
#    def __str__(self):
#        return self.tid

#    class Meta:
#        verbose_name = "教师"
#        verbose_name_plural = "教师"

#class Student(models.Model):

#    sid = models.AutoField(primary_key=True)
#    sname = models.CharField(max_length=128)
#    sdepart = models.CharField(max_length=128)
#    grade = models.CharField(max_length=128)
#    def __str__(self):
#        return self.sid

#    class Meta:
#        verbose_name = "学生"
#        verbose_name_plural = "学生"

#class Course(models.Model):

#    COMPULSORY = (
#        ('COMPULSORY', '必修'),
#        ('UNCOMPULSORY', "选修"),
#        ('UNKNOWN', "未知"),
#    )
#    cid = models.AutoField(primary_key=True)
#    cname = models.CharField(max_length=128)
#    credit = models.CharField(max_length=128)
#    is_compulsory = models.CharField(max_length=128,choices=COMPULSORY, default="未知")
#    target = models.IntField(max_length=11)
#    cdepart = models.CharField(max_length=128)
#    def __str__(self):
#        return self.cid

#    class Meta:
#        verbose_name = "课程"
#        verbose_name_plural = "课程"
