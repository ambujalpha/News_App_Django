from django.shortcuts import render, get_object_or_404, redirect
from .models import Main
from news.models import News
from cat.models import Cat
from subcat.models import SubCat


def home(request):

    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]

    return render(request, 'front/home.html', {'site': site, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews})


def about(request):

    site = Main.objects.get(pk=2)
    return render(request, 'front/about.html', {'site': site})


def panel(request):

    return render(request, 'back/home.html')

