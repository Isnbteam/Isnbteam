from django.shortcuts import render,redirect,HttpResponse
from app import models
from django.db.models import Count
import json
from django.forms import Form
from  django.forms import fields
from django.forms import widgets
# Create your views here.
def login(request):
    if request.method=="GET":
        return render(request,"login.html")
    else:
        username=request.POST.get("username")
        password=request.POST.get("password")
        user_obj=models.Userinfo.objects.filter(username=username,password=password)
        if user_obj:
            request.session["user"]={"user":username,"id":None}
            return redirect("/questionnaire/")
        else:pass
def student_login(request):
    if request.method=="GET":
        return render(request,"student_login.html")
    else:
        username=request.POST.get("username")
        password=request.POST.get("password")
        user_obj=models.Student.objects.filter(username=username,password=password).first()
        if user_obj:
            request.session["user"]={"user":user_obj.username,"id":user_obj.id}
            grade_id=user_obj.grade_id
            questionnaire_id=user_obj.grade.questionnaire_set.first().id
            return redirect("/student/%s/%s/"%(grade_id,questionnaire_id))

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
    if models.Userinfo.objects.filter(username=user["user"]):
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
def see_questionnaire(request,grade_id,questionnaire_id):
    """
    问卷发布内容
    :param request:
    :return:
    """
    user_id=request.session.get("user").get("id")

    #判断是不是本班学生

    if  not models.Student.objects.filter(id=user_id,grade_id=grade_id):
        return HttpResponse("你是不是想转班？")
    #判断是不是已经作答
    if models.Answer.objects.filter(student_id=user_id,question__questionnaire_id=questionnaire_id):
        return HttpResponse("你已经答过了！")
    #列出问题
    question_list=models.Question.objects.filter(questionnaire_id=questionnaire_id)
    question_dict={}
    for question in question_list:
        if question.types==1:
            question_dict["val_%s" % question.id]=fields.ChoiceField(
                label=question.caption,
                required=True,
                choices=[(i,i)for i in range(1,11)],
                error_messages={"required":"不能为空！"},
                widget=widgets.RadioSelect
            )
        elif question.types==2:
            question_dict["option_id_%s" % question.id] = fields.ChoiceField(
                required=True,
                label=question.caption,
                error_messages={"required": "不能为空！"},
                widget=widgets.RadioSelect,
                choices=models.Option.objects.filter(qs_id=question.id).values_list("id","name")
            )
        elif question.types==3:
            question_dict["content_%s" % question.id] = fields.CharField(
                required=True,
                label=question.caption,
                min_length=15,
                error_messages={"required": "不能为空！","min_length":"至少15字!"},
                widget=widgets.Textarea
            )

        else:return HttpResponse("滚一边去！")
    QuestionForm=type("QuestionForm",(Form,),question_dict)
    form=QuestionForm()
    if request.method=="GET":
        return render(request,"questionnaire_answer.html",{"form":form})
    else:
        form=QuestionForm(request.POST)
        if form.is_valid():
            objs=[]
            # {'option_id_1': '7', 'option_id_3': '1', 'val_4': '1', 'content_id_6': '一个很6666666666666666的人'}
            print(form.cleaned_data)
            for k,y in form.cleaned_data.items():
                types,question_id=k.rsplit("_",1)
                answer_dict={"student_id":user_id,"question_id":question_id,types:y}
                objs.append(models.Answer(**answer_dict))
            models.Answer.objects.bulk_create(objs)
            return HttpResponse("感谢您的参与！")
        else:
            return render(request,"questionnaire_answer.html",{"form":form})
def del_questionnaire(request,username,grade_id,questionnaire_id):
    #删除问题
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
    #删除选项
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