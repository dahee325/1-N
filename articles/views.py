from django.shortcuts import render, redirect
from .forms import ArticleForm, CommentForm
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
    comments = article.comment_set.all()
    # articles = Articles.objects.all()과 같은 코드
    form = CommentForm()

    context = {
        'article': article,
        'form': form,
        'comments': comments,
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


def delete(request, id):
    article = Article.objects.get(id=id)
    article.delete()

    return redirect('articles:index')


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