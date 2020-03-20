from django.shortcuts import render, get_object_or_404, redirect
from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage


def news_detail(request, word):

    site = Main.objects.get(pk=2)
    news = News.objects.filter(name=word)

    return render(request, 'front/news_detail.html', {'news': news, 'site': site})


def news_list(request):

    news = News.objects.all()

    return render(request, 'back/news_list.html', {'news': news})


def news_add(request):

    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newscat = request.POST.get('newscat')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')

        if newstitle == "" or newstxtshort == "" or newstxt == "":
            error = "All fields required"
            render(request, 'back/error.html', {'error': error})

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):

                if myfile.size < 5000000:

                    b = News(name=newstitle, date="2019", picname=filename, picurl=url, writer="-", catname=newscat, short_txt=newstxtshort, body_txt=newstxt, catid=0, show=0)
                    b.save()
                    return redirect('news_list')

                else:

                    error = "your file bigger than 5MB"
                    render(request, 'back/error.html', {'error': error})

            else:

                error = "your file not supported"
                render(request, 'back/error.html', {'error': error})

        except:
            error = "please input the image"
            render(request, 'back/error.html', {'error': error})

    return render(request, 'back/news_add.html')
