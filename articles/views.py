from django.shortcuts import render, redirect
from .forms import ArticleForm

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