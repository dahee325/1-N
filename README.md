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

## 2. modeling
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
- `articles/models.py` : `Article`클래스 생성
```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## migration
- `python manage.py makemigrations`
- `python manage.py migrate`