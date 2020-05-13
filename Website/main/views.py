from django.shortcuts import render, get_object_or_404, redirect
from .models import Main
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from trending.models import Trending
from django.contrib.auth.models import User, Group, Permission
import random
from random import randint
from manager.models import Manager
import string
from ipware import get_client_ip
from ip2geotools.databases.noncommercial import DbIpCity
from django.core.mail import send_mail
from django.conf import settings
from contactform.models import ContactForm
from zeep import Client
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
import urllib.request as urllib2
from rest_framework import viewsets
from .serializer import NewsSerializer
from django.http import JsonResponse
from newsletter.models import Newsletter

@csrf_exempt
def home(request):

    site = Main.objects.get(pk=2)
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]

    random_object = Trending.objects.all()[randint(0, len(trending) -1)]
    print(random_object)

    # Soup
    '''
    client = Client('xxxxxxxxxx.wsdl')
    result = client.service.funcname(1,2,3)
    print(result)
    '''

    #curl
    '''
    url = 'xxxxxxxxxxxxxxxx'
    payload = {'a':"b", 'c':"d"}
    result = requests.post(url, params=payload)
    print(result.url)
    print(result)
    '''

    #json
    '''
    url = 'xxxxxxxxxxxx'
    data = {'a': "b", 'c': "d"}
    headers = {'Content-Type':'application/json','API_KEY':'xxxxxxxxxxx'}
    result = requests.post(url,data=json.dumps(data),headers=headers)
    print(result)
    '''

    my_html = """
        
    <title> This is a test </title>
    <mytag>test</mytag>
    
    """
    # soup = BeautifulSoup(my_html, 'html.parser')
    # print(soup.title)

    '''
    url='https://djangolearn.xyz/'
    result = request.post(url)
    soup = BeautifulSoup(result.content, 'html.parser')
    #print(soup.title.sring)
    '''

    '''
    url = 'https://djangolearn.xyz/'
    opener = urllib2.build_opener()
    content = opener.open(url).read()
    soup = BeautifulSoup(content)
    print(soup.title.sring)
    '''

    '''
    url = 'http://127.0.0.1:8000/show/data/'
    opener = urllib2.build_opener()
    content = opener.open(url).read()
    print(content)
    '''

    request.session['test'] = "hello"

    print(request.session['test'])

    return render(request, 'front/home.html', {'site': site, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews': popnews, 'popnews2': popnews2, 'trending': trending, 'lastnews2': lastnews2})


def about(request):

    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]

    return render(request, 'front/about.html', {'site': site, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews2': popnews2, 'trending': trending})


def panel(request):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    perm = 0
    perms = Permission.objects.filter(user=request.user)
    for i in perms:
        if i.codename == "master_user": perm =1

    '''
    test = ['!', '@', '#', '$', '%']
    rand = ""
    for i in range(4):
        rand += random.choice(string.ascii_letters)
        rand += random.choice(test)
        rand += str(random.randint(0,9))
        
    count = News.objects.count()
    rand = News.objects.all()[randint(0,count-1)]
    '''

    return render(request, 'back/home.html', {})


def mylogin(request):

    if request.method == 'POST' :

        utxt = request.POST.get('username')
        ptxt = request.POST.get('password')

        if utxt != "" and ptxt != "" :

            user = authenticate(username= utxt, password= ptxt)

            if user != None :

                login(request, user)
                return redirect('panel')

    return render(request, 'front/login.html')


def myregister(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if name == "":
            msg = "Input name"
            return render(request, 'front/msgbox.html', {'msg': msg})

        if password1!=password2 :
            msg = "Your password didn't match"
            return render(request, 'front/msgbox.html', {'msg': msg})

        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0

        for i in password1:

            if i > "0" and i < "9":
                count1 += 1
            if i > "A" and i < "Z":
                count2 += 1
            if i > "a" and i < "z":
                count3 += 1
            if i > "!" and i < "(":
                count4 += 1

        if count1 == 0 and count2 == 0 and count3 == 0 and count4 == 0 :
            msg = "Your password didn't match"
            return render(request, 'front/msgbox.html', {'msg': msg})

        if len(password1)<8:
            msg = "Your password didn't match"
            return render(request, 'front/msgbox.html', {'msg': msg})

        if len(User.objects.filter(username=uname))==0 and len(User.objects.filter(email=email)) == 0 :

            ip, is_routable = get_client_ip(request)

            if ip is None:
                ip = "0.0.0.0"

            try:
                response = DbIpCity.get(ip, api_key='free')
                country = response.country + " | " + response.city

            except:
                country = "Unknown"

            user = User.objects.create_user(username=uname, email=email, password=password1)
            b = Manager(name=name, utxt=uname, email=email, ip=ip, country=country)
            b.save()

    return render(request, 'front/login.html')


def mylogout(request):

    logout(request)

    return redirect('mylogin')


def site_setting(request):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error': error})

    if request.method == 'POST' :

        name = request.POST.get('name')
        tell = request.POST.get('tell')
        fb = request.POST.get('fb')
        tw = request.POST.get('tw')
        yt = request.POST.get('yt')
        link = request.POST.get('link')
        txt = request.POST.get('txt')
        seo_txt = request.POST.get('seotxt')
        seo_keywords = request.POST.get('seokeyword')

        if fb == "":
            fb = "#"
        if tw == "":
            tw = "#"
        if yt == "":
            yt = "#"
        if link == "":
            link = "#"

        if name == "" or tell == "" or txt == "":
            error = "All fields required"
            return render(request, 'back/error.html', {'error': error})

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            picurl = url
            picname = filename

        except:

            picurl = "-"
            picname = "-"

        try:
            myfile2 = request.FILES['myfile2']
            fs2 = FileSystemStorage()
            filename2 = fs2.save(myfile2.name, myfile2)
            url2 = fs2.url(filename2)

            picurl2 = url2
            picname2 = filename2

        except:

            picurl2 = "-"
            picname2 = "-"

        b = Main.objects.get(pk=2)
        b.name = name
        b.tell = tell
        b.fb = fb
        b.tw = tw
        b.yt = yt
        b.link = link
        b.about = txt
        b.seo_txt = seo_txt
        b.seo_keywords = seo_keywords

        if picurl != "-" :
            b.picurl = picurl
        if picname != "-" :
            b.picname = picname
        if picurl2 != "-":
            b.picurl2 = picurl2
        if picname2 != "-":
            b.picname2 = picname2

        b.save()

    site = Main.objects.get(pk=2)

    return render(request, 'back/setting.html', {'site': site})


def about_setting(request):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error': error})

    if request.method == 'POST':

        txt = request.POST.get('txt');

        if txt == "":
            error = "Something Wrong"
            return render(request, 'back/error.html', {'error': error})

        b = Main.objects.get(pk=2)
        b.abouttxt = txt
        b.save()

    about = Main.objects.get(pk=2).abouttxt

    return render(request, 'back/about_setting.html', {'about': about})


def contact(request):

    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]

    return render(request, 'front/contact.html',{'site': site, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews2': popnews2, 'trending': trending})


def change_pass(request):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    if request.method == 'POST':

        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')

        if oldpass == "" or newpass == "":
            error = "All fields required"
            return render(request, 'back/error.html', {'error': error})

        user = authenticate(username=request.user, password=oldpass)
        if user != None:

            if len(newpass) < 8:
                error = "less character"
                return render(request, 'back/error.html', {'error': error})

            count1 = 0
            count2 = 0
            count3 = 0
            count4 = 0
            for i in newpass:

                if i > "0" and i < "9":
                    count1 += 1
                if i > "A" and i < "Z":
                    count2 += 1
                if i > "a" and i < "z":
                    count3 += 1
                if i > "!" and i < "(":
                    count4 += 1

            if count1 == 1 and count2 == 1 and count3 == 1 and count4 == 1:

                user = User.objects.get(username=request.user)
                user.set_password(newpass)
                user.save()
                return redirect('mylogout')

        else:
            error = "Wrong password"
            return render(request, 'back/error.html', {'error': error})

    return render(request, 'back/changepass.html')


def answer_cm(request, pk):

    if request.method == 'POST':

        txt = request.POST.get('txt')

        if txt == "":
            error = "Type Your Answer"
            return render(request, 'back/error.html', {'error': error})

        to_email = ContactForm.objects.get(pk=pk).email

        '''
        subject = 'answer_form'
        message = txt
        email_from = settings.EMAIL_HOST_USER
        emails = [to_email]
        send_mail(subject, message, email_from, emails)
        '''

        send_mail(
            'sender number 2',
            txt,
            'sender@djangolearn.xyz',
            [to_email],
            fail_silently=False,
        )

    return render(request, 'back/answer_cm.html', {'pk':pk})


class NewsViewSet(viewsets.ModelViewSet):

    queryset = News.objects.all()
    serializer_class = NewsSerializer


def show_data(request):

    count = Newsletter.objects.filter(status=1).count()

    data = {'Count':count}

    return JsonResponse(data)