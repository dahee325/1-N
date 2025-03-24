# 0. setting
- `python -m venv venv`
- `source venv/Scripts/activate`
- `pip install django`
- `.gitignore` : python, windows, macOS, django

## 데이터 베이스 정규화
- 목표 : 테이블 간에 중복된 데이터를 제거하는 것
- 삽입이상, 갱신이상, 삭제이상

# 1. 프로젝트 생성
- `django-admin startproject board .` : board 프로젝트 생성
- `django-admin startapp articles` : articles 앱 생성
- `board/settings.py` : articles 앱 등록
