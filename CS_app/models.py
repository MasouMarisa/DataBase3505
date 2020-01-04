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
