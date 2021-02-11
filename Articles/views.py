from django.shortcuts import render

# Create your views here.
from Articles.models import New, FAQ


def articles(request):
    new_articles = New.objects.order_by("-pub_date")[:10]

    return render(request, 'articles/articles.html',
                  context={"page_title": 'Новости', 'articles': new_articles})


def faq(request):
    return render(request=request,
                  template_name='articles/FAQ.html',
                  context={'page_title': 'FAQ', 'FAQ': FAQ.objects.all()[::-1]}
                  )
