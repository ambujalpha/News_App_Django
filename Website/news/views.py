from django.shortcuts import render, get_object_or_404, redirect
from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
from cat.models import Cat
from trending.models import Trending


def news_detail(request, word):

    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]

    shownews = News.objects.filter(name=word)
    popnews = News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]

    tagname = News.objects.get(name=word).tag
    tag = tagname.split(',')

    try:

        mynews = News.objects.get(name=word)
        mynews.show = mynews.show + 1
        mynews.save()

    except:

        print("Can't add show")

    return render(request, 'front/news_detail.html',  {'site': site, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'shownews': shownews, 'popnews': popnews, 'popnews2': popnews2, 'tag': tag, 'trending': trending})


def news_list(request):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    news = News.objects.all()

    return render(request, 'back/news_list.html', {'news': news})


def news_add(request):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    if len(str(day)) == 1:
        day = "0"+str(day)
    if len(str(month)) == 1:
        month = "0"+str(month)

    today = str(year) + "/" + str(month) + "/" + str(day)
    time = str(now.hour) + "/" + str(now.minute)

    cat = SubCat.objects.all()

    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newscat = request.POST.get('newscat')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        newsid = request.POST.get('newscat')
        tag = request.POST.get('tag')

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):

                if myfile.size < 5000000:

                    newsname = SubCat.objects.get(pk=newsid).name
                    ocatid = SubCat.objects.get(pk=newsid).catid

                    b = News(name=newstitle, date=today, picname=filename, picurl=url, writer="-", catname=newsname, short_txt=newstxtshort, body_txt=newstxt, catid=newsid, show=0, time=time, ocatid=ocatid, tag=tag)
                    b.save()

                    count = len(News.objects.filter(ocatid=ocatid))

                    b = Cat.objects.get(pk=ocatid)
                    b.count = count
                    b.save()

                    return redirect('news_list')

                else:

                    error = "your file bigger than 5MB"
                    print(error)
                    render(request, 'back/error.html', {'error': error})

            else:
                fs = FileSystemStorage()
                fs.delete(filename)
                error = "your file not supported"
                print(error)
                render(request, 'back/error.html', {'error': error})

        except :

            error = "please input the image"
            print(error)
            render(request, 'back/error.html', {'error': error})

    return render(request, 'back/news_add.html', {'cat': cat})


def news_delete(request, pk):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    try:
        b = News.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(b.picname)
        b.delete()

        ocatid = News.objects.get(pk=pk).ocatid

        count = len(News.objects.filter(ocatid=ocatid))

        m = Cat.objects.get(pk=ocatid)
        m.count = count
        m.save()

    except:
        error = "Something Wrong"
        return render(request, 'back/error.html', {'error': error})

    return redirect('news_list')


def news_edit(request, pk):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    if len(str(News.objects.get(pk=pk))) == 0:
        error = "News not found"
        return render(request, 'back/error.html', {'error': error})

    news = News.objects.get(pk=pk)
    cat = SubCat.objects.all()

    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newscat = request.POST.get('newscat')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        newsid = request.POST.get('newscat')
        tag = request.POST.get('tag')

        try:

            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):

                if myfile.size < 5000000:

                    newsname = SubCat.objects.get(pk=newsid).name

                    b = News.objects.get(pk=pk)

                    fss = FileSystemStorage()
                    fss.delete(b.picname)

                    b.name = newstitle
                    b.short_txt = newstxtshort
                    b.body_txt = newstxt
                    b.picname = filename
                    b.picurl = url
                    b.catname = newsname
                    b.catid = newsid
                    b.tag = tag

                    b.save()

                    return redirect('news_list')

                else:

                    error = "your file bigger than 5MB"
                    print(error)
                    render(request, 'back/error.html', {'error': error})

            else:
                fs = FileSystemStorage()
                fs.delete(filename)
                error = "your file not supported"
                print(error)
                render(request, 'back/error.html', {'error': error})

        except :

            newsname = SubCat.objects.get(pk=newsid).name

            b = News.objects.get(pk=pk)

            fss = FileSystemStorage()
            fss.delete(b.picname)

            b.name = newstitle
            b.short_txt = newstxtshort
            b.body_txt = newstxt
            b.catname = newsname
            b.catid = newsid
            b.tag = tag

            b.save()

            return redirect('news_list')

    return render(request, 'back/news_edit.html', {'pk': pk, 'news': news, 'cat': cat})
