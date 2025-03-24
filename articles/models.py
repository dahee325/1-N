from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE) # article : 나보다 한단계 위의 부모모델(게시물)
    # => ForeignKey() : Article모델과 Comment모델이 1:N 관계로 연결된다는 것을 의미
    # => on_delete 옵션을 필수도 설정해야함 / CASCADE : 부모모델의 데이터가 지워지면 자식모델의 데이터도 자동으로 지워짐