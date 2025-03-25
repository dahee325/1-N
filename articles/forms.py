from django.forms import ModelForm
from django import forms
from .models import Article, Comment

class ArticleForm(ModelForm):
    title = forms.CharField( # title 덮어씌우기
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    class Meta():
        model = Article
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CommentForm(ModelForm):
    class Meta():
        model = Comment
        # fields = '__all__'
        
        # fields : 추가할 필드 목록
        # fields = ('content', ) # 튜플로 설정, content와 article 중 content만 선택

        # exclude : 제외할 필드 목록
        exclude = ('article', ) # article만 제외