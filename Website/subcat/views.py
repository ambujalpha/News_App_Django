from django.shortcuts import render, get_object_or_404, redirect
from .models import SubCat


def subcat_list(request):

    subcat = SubCat.objects.all()
    return render(request, 'back/subcat_list.html', {'subcat': subcat})


def subcat_add(request):

    if request.method == 'POST':

        name = request.POST.get('name')

        if name == "":

            error = "All fields required"
            return render(request, 'back/error.html', {'error': error})

        if len(SubCat.objects.filter(name=name)) != 0 :

            error = "This name is used"
            return render(request, 'back/error.html', {'error': error})

    return render(request, 'back/subcat_add.html')
