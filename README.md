# 데이터 베이스 정규화
- 목표 : 테이블 간에 중복된 데이터를 제거하는 것
- 삽입이상, 갱신이상, 삭제이상

## 0. setting
- `python -m venv venv`
- `source venv/Scripts/activate`
- `pip install django`
- `.gitignore` : python, windows, macOS, django

## 1. 프로젝트 생성
- `django-admin startproject board .` : board 프로젝트 생성
- `django-admin startapp articles` : articles 앱 생성
- `board/settings.py` : articles 앱 등록

## 2. 공통 base.html 설정
- 최상단 폴더에 `templates` 폴더 생성
- `1-N/templates` 폴더에 `base.html`파일 생성 => `board/settings.py`에 `templates` 폴더 연결
- `templates/base.html` : 빈 블록 만들기
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    {% block body %}

    {% endblock %}
</body>
</html>
```

## 3. modeling
- `articles/models.py` : `Article`클래스 생성
```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## 4. migration
- `python manage.py makemigrations`
- `python manage.py migrate`

## 5. 기본 url설정
- `board/urls.py` : 경로 설정
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls'))
]
```

## 6. Create
- `articles` 폴더 안에 `urls.py` 파일 생성
```python
from django.urls import path
from . import views

app_name = 'articles'

urlspatterns = [
    # Create
    path('create/', views.create, name='create'),
]
```
- `articles/forms.py` : **모델 폼 만들기**, html코드를 python으로 만들기(유효성 기능을 사용하기 위해서)
```python
from django.forms import ModelForm
from .models import Article

class ArticleForm(ModelForm):
    class Meta():
        model = Article
        fields = '__all__'
```
- `board/views.py`
```python
from django.shortcuts import render
from .forms import ArticleForm

# Create your views here.
def create(request):
    if request.method == 'POST': # 데이터를 담아서 보내기
        pass
    else: # 빈 종이 보여주기
        form = ArticleForm():
    
    context = {
        'form': form,
    }

    return render(request, 'create.html', context)
```
- `articles` 폴더 안에 `templates` 폴더 생성
- `articles/templates`폴더 안에 `create.html` 파일 생성
```html
{% extends 'base.html' %}

{% block body %}
<form action="" method="POST">
    {% csrf_token %} <!--method="POST"이면 작성해야함-->
    {{form}}
    <input type="submit">
</form>
{% endblock %}
```
- `articles/views.py` : if문 채우기
```python
from django.shortcuts import render, redirect
from .forms import ArticleForm

def create(request):
    if request.method == 'POST': # 데이터를 담아서 보내기
        form = ArticleForm(request.POST) # 사용자의 정보를 담은 ArticleForm
        if form.is_valid():
            form.save()
            return redirect('articles:index') # 아직 index를 만들지는 않음
    ...
```
-
## 7. Read(ALL)
- `articles/urls.py`
```python
urlpatterns = [
    # Create
    path('create/', views.create, name='create'),
    # Read
    path('', views.index, name='index'),
]
```
- `articles/views.py`
```python
from .models import Article

def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles,
    }
    
    return render(request, 'index.html', context)
```
- `articles/templates` 폴더 안에 `index.html` 파일 생성
```html
{% extends 'base.html' %}

{% block body %}
    {% for article in articles %}
    <h3>{{article.title}}</h3>
    {% endfor %}
{% endblock %}
```

## 8. Read(1)
- `articles/templates/index.html`
```html
{% extends 'base.html' %}

{% block body %}
    {% for article in articles %}
    <h3>{{article.title}}</h3>
    <a href="{% url 'articles:detail' article.id %}">detail</a>
    {% endfor %}
{% endblock %}
```
- `articles/urls.py`
```python
urlpatterns = [
    # Create
    path('create/', views.create, name='create'),
    # Read
    path('', views.index, name='index'),
    path('<int:id>', views.detail, name='detail'),
]
```
- `articles/views.py`
```python
def detail(request, id):
    article = Article.objects.get(id=id)

    context = {
        'article': article,
    }

    return render(request, 'detail.html', context)
```
- `articles/templates/detail.html`
```html
{% extends 'base.html' %}

{% block body %}

    <h3>{{article.title}}</h3>
    <p>{{article.content}}</p>
    <p>{{article.created_at}}</p>
    <p>{{article.updated_at}}</p>

{% endblock %}
```

## 9. Update
- `articles/templates/detail.html`
```html
{% extends 'base.html' %}

{% block body %}
    ...
    <a href="{% url 'articles:update' article.id %}">update</a>
{% endblock %}
```
- `articles/urls.py`
```python
urlpatterns = [
    # Create
    path('create/', views.create, name='create'),
    # Read
    path('', views.index, name='index'),
    path('<int:id>', views.detail, name='detail'),
    # Update
    path('<int:id>/update/', views.update, name='update'),
]
```
- `articles/views.py`
```python
def update(request, id):
    if request.method == 'POST':
        pass
    else:
        article = Article.objects.get(id=id)
        form = ArticleForm(instance=article) # instance= : ModelForm의 옵션
    
    context = {
        'form': form,
    }

    return render(request, 'update.html', context)
```
- `articles/templates/update.html`
```html
{% extends 'base.html' %}

{% block body %}
    <form action="" method="POST">
        {% csrf_token %}
        {{form}}
        <input type="submit">
    </form>
{% endblock %}
```
- `articles/views.py` : if문 채우기
```python
def update(request, id):
    article = Article.objects.get(id=id) # if문과 else문 모두 필요하므로 if문 밖으로 뺌

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article) # (새로운 정보, 기존 정보)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', id=id) #id=id, id=article.id 같음
    ...
```
- 