from django.shortcuts import render,redirect,HttpResponse
from app import models
from django.db.models import Count
import json
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
def student_login(request):
    if request.method=="GET":
        return render(request,"login.html")
    else:
        username=request.POST.get("username")
        password=request.POST.get("password")
        user_obj=models.Student.objects.filter(username=username,password=password)
        if user_obj:
            request.session["user"]={"user":username,"id":user_obj.id}
            return redirect("/see_questionnaire/")
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
        return render(request, "edit_Question.html",{"type_list":type_list,"question_list":question_list,"questionnaire":questionnaire})
    else:
        quest_list=json.loads(request.body.decode('utf-8'))
        # print(quest_list)
        response={}
        for quest in quest_list:
            questions_id = quest.get("questions_id")#问题id
            quest_caption = quest.get("quest_caption")
            print(quest_caption)
            if len(quest_caption)==0:
                response["is_success"]=False
                response["error"] = "问题不能为空！"
                return HttpResponse(json.dumps(response))
            quest_type = quest.get("quest_type")
            options = quest.get("options")
            # print(options)
            if questions_id!="None" and models.Question.objects.filter(id=questions_id):#如果是已有问题
                if options:#如果有选项，即单选，type==2，见网页157行
                        models.Question.objects.filter(id=questions_id).update(caption=quest_caption,types=quest_type)
                        for i in options:
            #                 {"opp_id":opp_id,"content":content,"score":score}
                            opp_id=i.get("opp_id")#选项id
                            content=i.get("content")

                            score=i.get("score")
                            if len(content)==0 or len(score)==0:
                                response["is_success"] = False
                                response["error"]="选项内容和分值不能为空！"
                                return HttpResponse(json.dumps(response))
                            else:
                                if opp_id and  models.Option.objects.filter(id=opp_id):
                                    models.Option.objects.filter(id=opp_id).update(name=content,score=score)
                                else:
                                    models.Option.objects.create(name=content,score=score,qs_id=questions_id)
                else:
                     models.Question.objects.filter(id=questions_id).update(caption=quest_caption,types=quest_type)
            elif questions_id=="None":#新问题
                if options:  # 如果有选项，即单选，type==2，见网页157行
                    questions_obj=models.Question.objects.create(caption=quest_caption, types=quest_type,
                                                   questionnaire_id=questionnaire_id)
                    for i in options:
                        # opp_id = i.get("opp_id")
                        contents = i.get("content")
                        scores= i.get("score")
                        if len(content) == 0 or len(score) == 0:
                            response["is_success"] = False
                            response["error"] = "选项内容和分值不能为空！"
                            return HttpResponse(json.dumps(response))
                        else:

                            models.Option.objects.create(name=contents, score=scores, qs_id=questions_obj.id)
                else:
                    models.Question.objects.create(caption=quest_caption, types=int(quest_type),
                                                   questionnaire_id=questionnaire_id)
        response["is_success"]=True
        return HttpResponse("ok")
def see_questionnaire(request,username,grade_id,questionnaire_id):
    """
    问卷发布内容
    :param request:
    :return:
    """
    pass
def del_questionnaire(request,username,grade_id,questionnaire_id):
    question_id=request.POST.get("question_id")
    obj=models.Question.objects.filter(id=question_id)
    response={}
    if obj:
        obj.delete()
        response["is_success"]=True
        return HttpResponse(json.dumps(response))
    else:
        response["is_success"] = True
        return HttpResponse(json.dumps(response))
def del_question(request,username,grade_id,questionnaire_id):
    option_id=request.POST.get("option_id")
    obj=models.Option.objects.filter(id=option_id)
    response = {}
    if obj:
        obj.delete()
        response["is_success"] = True
        return HttpResponse(json.dumps(response))
    else:
        response["is_success"] = True
        return HttpResponse(json.dumps(response))