from django import forms
from django.forms import widgets

class QuestionForm(forms.Form):
    question=forms.CharField(
        required=True,
        max_length=64,
        error_messages={"required":"不能为空","max_length":"至多64！"},
        widget=widgets.TextInput(attrs={"class":"form-control" ,"placeholder":"问题"}),


    )
    questiontype=forms.ChoiceField(
        choices=( (1, '打分'),
        (2, '单选'),
        (3, '评价'),),
        widget=widgets.Select(attrs={"class":"form-control","size":1}),
        initial = 1,
    )