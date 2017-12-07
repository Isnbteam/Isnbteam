from django.shortcuts import render,redirect,HttpResponse
from app import models
from app.QuestionForm import QuestionForm
# Create your views here.
def login(request):
    if request.method=="GET":
        return render(request,"login.html")
    else:
        username=request.POST.get("username")
        password=request.POST.get("password")
        user_obj=models.Userinfo.objects.filter(username=username,password=password)
        if user_obj:
            request.session["user"]=username
            return redirect("/questionnaire/")
        else:pass
def question(request):
    """
    问题列表
    :param request:
    :return:
    """
    user=request.session.get("user")
    if models.Userinfo.objects.filter(username=user):
        if request.method == "GET":
            return render(request, "edit_Question.html")
    else:
        return redirect("/login/")
def questionnaire(request):
    """
    问卷列表
    :param request:
    :return:
    """
    user = request.session.get("user")
    if models.Userinfo.objects.filter(username=user):
        if request.method == "GET":
            class Foo(object):
                def __init__(self, data):
                    self.data = data

                def __iter__(self):
                    for item in self.data:
                        yield item
            questionnaire_list=models.Questionnaire.objects.all()
            obj=Foo(questionnaire_list)

            return render(request, "Questionnaire.html",{"questionnaire_list":obj})
    else:
        return redirect("/login/")
def edit_questionnaire(request,username,grade_id,questionnaire_id):
    """
    问卷编辑
    :param request:
    :return:
    """
    if request.method == "GET":
        questionnaire=models.Questionnaire.objects.filter(id=questionnaire_id).first()
        question_list=questionnaire.question_set.all()
        type_list=[
            {"id":1,"type":"打分"},
            {"id":2,"type":"单选"},
            {"id":3,"type":"评价"},
        ]
        return render(request, "edit_Question.html",{"type_list":type_list,"question_list":question_list})
    else:pass
def see_questionnaire(request,username,grade_id,questionnaire_id):
    """
    问卷发布内容
    :param request:
    :return:
    """
    pass