from django.shortcuts import render, get_object_or_404, redirect
from .models import Main
from news.models import News
from cat.models import Cat


def home(request):

    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()

    return render(request, 'front/home.html', {'site': site, 'news': news, 'cat': cat})


def about(request):

    site = Main.objects.get(pk=2)
    return render(request, 'front/about.html', {'site': site})


def panel(request):

    return render(request, 'back/home.html')

