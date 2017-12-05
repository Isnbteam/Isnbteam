from django.contrib import admin

# Register your models here.
from app.models import *
admin.site.register(Userinfo)
admin.site.register(Student)
admin.site.register(Question)
admin.site.register(Questionnaire)
admin.site.register(Grade)
admin.site.register(Option)
admin.site.register(Answer)