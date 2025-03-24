from django.shortcuts import render, redirect
from .forms import ArticleForm
from .models import Article

# Create your views here.
def create(request):
    if request.method == 'POST': # 데이터를 담아서 보내기
        form = ArticleForm(request.POST) # 사용자의 정보를 담은 ArticleForm
        if form.is_valid():
            form.save()
            return redirect('articles:index') # 아직 index를 만들지는 않음

    else: # 빈 종이 보여주기
        form = ArticleForm()

    context = {
        'form': form,
    }

    return render(request, 'create.html', context)


def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles,
    }

    return render(request, 'index.html', context)


def detail(request, id):
    article = Article.objects.get(id=id)

    context = {
        'article': article,
    }

    return render(request, 'detail.html', context)


def update(request, id):
    article = Article.objects.get(id=id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article) # (새로운 정보, 기존 정보)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', id=id) #id=id, id=article.id 같음

    else:
        form = ArticleForm(instance=article) # instance= : ModelForm의 옵션, 기존 정보를 알려줌
    
    context = {
        'form': form,
    }

    return render(request, 'update.html', context)