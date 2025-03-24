# 데이터 베이스 정규화
- 목표 : 테이블 간에 중복된 데이터를 제거하는 것
- 삽입이상, 갱신이상, 삭제이상
- 게시물, 댓글 CRUD 만들기 => 두개의 CRUD 생성
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

# 게시물
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
- `articles/templates/detail.html` : update 버튼 생성
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

## 10. Delete
- `articles/templates/detail.html` : delete 버튼 생성
```html
{% extends 'base.html' %}

{% block body %}
    ...
    <a href="{% url 'articles:update' article.id %}">update</a>
    <a href="{% url 'articles:delete' article.id %}">delete</a>
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
    # Delete
    path('<int:id>/delete/', views.delete, name='delete'),
]
```
- `articles/views.py`
```python
def delete(request, id):
    article = Article.objects.get(id=id)
    article.delete()

    return redirect('articles:index')
```

# 댓글
## 1. modeling
- `articles/models.py`
    - [Relationship fields](https://docs.djangoproject.com/en/5.1/ref/models/fields/#module-django.db.models.fields.related) : models.ForeignKey
    - [on_delete](https://docs.djangoproject.com/en/5.1/ref/models/fields/#django.db.models.ForeignKey.on_delete) : models.ForeingKey의 필수 옵션\
    => PROTECT : 게시물에 댓글이 달려있으면 게시물을 지울 수 없음
    => SET_DEFAULT : ghost계정을 만들어서 지우게되면 코드들이 저장됨
```python
class Comment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    # article : 나보다 한단계 위의 부모모델(게시물) / article이 실제로 저장하는 것은 article_id
    # => ForeignKey() : Article모델과 Comment모델이 1:N 관계로 연결된다는 것을 의미
    # => on_delete 옵션을 필수도 설정해야함
```

## 2. migration
- `python manage.py makemigrations`
- `python manage.py migrate`

## 3. 댓글폼 만들기
- `articles/forms.py`
```python
from django.forms import ModelForm
from .models import Article, Comment

...

class CommentForm(ModelForm):
    class Meta():
        model = Comment
        fields = '__all__'
```
- `articles/views.py` : detail함수에다가 댓글폼만들기
```python
from django.shortcuts import render, redirect
from .forms import ArticleForm, CommentForm
from .models import Article

...

def detail(request, id):
    article = Article.objects.get(id=id)
    form = CommentForm()

    context = {
        'article': article,
        'form': form,
    }

    return render(request, 'detail.html', context)
```
- `articles/templates/detail.html`
```html
{% block body %}

    ...
    <hr>

    {{form}}

{% endblock %}
```
- `articles/forms.py` : content와 article 중 content만 나타나게 설정(article은 안보이게)
```python
from django.forms import ModelForm
from .models import Article, Comment

...
class CommentForm(ModelForm):
    class Meta():
        model = Comment
        # fields = '__all__'

        # fields : 추가할 필드 목록
        # fields = ('content', ) # 튜플로 설정, content와 article 중 content만 선택

        # exclude : 제외할 필드 목록
        exclude = ('article', ) # article만 제외
```
- `articles/templates/detail.html`
```html
{% block body %}

    ...

    <hr>
    <form action="" method="POST">
        {% csrf_token %}
        {{form}}
        <input type="submit">
    </form>

{% endblock %}
```

## 4. 댓글 제출 경로 설정
- `articles/templates/detail.html`
```html
{% block body %}

    ...
    <form action="{% url 'articles:comment_create' article.id %}" method="POST">
        {% csrf_token %}
        {{form}}
        <input type="submit">
    </form>

{% endblock %}
```

## 5. Comment Create
- `articles/views.py`
```python
urlpatterns = [
    ...

    # Comment
    # Create
    path('<int:article_id>/comments/create/', views.comment_create, name='comment_create') # 'articles/10/comments/create/'
]
```
- `articles/views.py`
```python
def comment_create(request, article_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # commit=False : 데이터를 완전히 저장 X (임시저장)
            # => article은 안보이게 설정했기 때문에 article_id가 비어있음
            
            article = Article.objects.get(id=article_id) # article_id 지정
            comment.article = article
            comment.save() # 댓글 저장

            return redirect('articles:detail', id=article_id)

    else:
        return redirect('articles:index')
```

## 6. Comment Read
- `articles/views.py`
```python
def detail(request, id):
    article = Article.objects.get(id=id)
    comments = article.comment_set.all()
    # articles = Articles.objects.all()과 같은 코드
    # => 여기서 comments를 안만들고 detail.html에서 article.comment_set.all을 바로 사용하는 경우가 대부분
    form = CommentForm()

    context = {
        'article': article,
        'form': form,
        'comments': comments,
    }

    return render(request, 'detail.html', context)
```
- `articles/templates/detail.html`
```html
{% block body %}

    ...
    <hr>

    {% for comment in comments %}
    {% endfor %}

{% endblock %}
```

## 7. Comment Update
- 수정하는 페이지를 현재 페이지로 두고 수정해야함 => 자바 스크립트 사용

## 8. Comment Delete
- `articles/templates/detail.html`
```html
{% block body %}

    ...

    {% for comment in comments %}
        <li>{{comment.content}}</li>
        <a href="{% url 'articles:comment_delete' article.id comment.id %}">delete</a>
    {% endfor %}

{% endblock %}
```
- `articles/urls.py`
```python
urlpatterns = [
    ...

    # Comment
    # Create
    path('<int:article_id>/comments/create/', views.comment_create, name='comment_create'), # 'articles/10/comments/create/'
    # Delete
    path('<int:article_id>/comments/<int:id>/delete/', views.comment_delete, name='comment_delete'),
]
```
- `articles/views.py`
```python
from django.shortcuts import render, redirect
from .forms import ArticleForm, CommentForm
from .models import Article, Comment

def comment_delete(request, article_id, id):
    comment = Comment.objects.get(id=id)
    comment.delete()

    return redirect('articles:detail', id=article_id)
```