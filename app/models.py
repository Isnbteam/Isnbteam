from django.db import models

# Create your models here.
class Userinfo(models.Model):
    """
    员工表
    """
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    grade=models.ForeignKey(to="Grade",verbose_name="班级")
    class Meta:
        verbose_name_plural="员工表"
    def __str__(self):
        return self.username

class Student(models.Model):
    """
    学生表
    """
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    grade=models.ForeignKey(to="Grade",verbose_name="班级")
    class Meta:
        verbose_name_plural="学生表"
    def __str__(self):
        return self.username

class Grade(models.Model):
    """
    班级表
    """
    title=models.CharField(max_length=32)
    class Meta:
        verbose_name_plural="班级表"
    def __str__(self):
        return self.title
class Questionnaire(models.Model):
    """
    问卷表
    """
    caption=models.CharField(max_length=32)
    grade=models.ForeignKey(to="Grade",verbose_name="班级")
    creator = models.ForeignKey(to=Userinfo)
    class Meta:
        verbose_name_plural="问卷表"
    def __str__(self):
        return self.caption
class Question(models.Model):
    """
    问题表
    """
    caption=models.CharField(max_length=64)
    question_types = (
        (1, '打分'),
        (2, '单选'),
        (3, '评价'),
    )
    types = models.IntegerField(choices=question_types)
    class Meta:
        verbose_name_plural="问题表"
    def __str__(self):
        return self.caption

class Option(models.Model):
    """
    单选题的选项
    """
    name = models.CharField(verbose_name='选项名称',max_length=32)
    score = models.IntegerField(verbose_name='选项对应的分值')
    qs = models.ForeignKey(to=Question)
    class Meta:
        verbose_name_plural="单选题的选项"
    def __str__(self):
        return self.name

class Answer(models.Model):
    """
    回答
    """
    student = models.ForeignKey(to=Student)
    question = models.ForeignKey(to=Question,verbose_name="问题")

    val = models.IntegerField(null=True,blank=True)
    content = models.CharField(max_length=255,null=True,blank=True)
    class Meta:
        verbose_name_plural="回答"
    def __str__(self):
        return self.student.username