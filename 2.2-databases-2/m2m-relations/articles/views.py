from django.shortcuts import render
from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    ordering = '-published_at'

    # Получаем статьи, отсортированные по дате публикации.
    # prefetch_related('scopes__tag') загружает все связанные разделы и теги 
    # за один дополнительный запрос, что сильно ускоряет работу страницы.
    articles = Article.objects.order_by(ordering).prefetch_related('scopes__tag')

    context = {
        'object_list': articles
    }

    return render(request, template, context)