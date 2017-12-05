from django.shortcuts import render,redirect,HttpResponse
from app import models
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
            return redirect("/question/")
        else:pass
def question(request):
    user=request.session.get("user")
    if models.Userinfo.objects.filter(username=user):
        if request.method == "GET":
            return render(request, "Question.html")
    else:
        return redirect("/login/")