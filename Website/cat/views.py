from django.shortcuts import render, get_object_or_404, redirect
from .models import Cat
import csv
from django.http import HttpResponse

def cat_list(request):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    cat = Cat.objects.all()
    return render(request, 'back/cat_list.html', {'cat': cat})


def cat_add(request):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    if request.method == 'POST':

        name = request.POST.get('name')

        if name == "":

            error = "All fields required"
            return render(request, 'back/error.html', {'error': error})

        if len(Cat.objects.filter(name=name)) != 0 :

            error = "This name is used"
            return render(request, 'back/error.html', {'error': error})

        b = Cat(name=name)
        b.save()
        return redirect('cat_list')

    return render(request, 'back/cat_add.html')


def export_cat_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cat.csv" '

    writer = csv.writer(response)
    writer.writerow(['Title','Counter'])

    for i in Cat.objects.all():
        writer.writerow([i.name, i.count])

    return response

def import_cat_csv(request):

    if request.method == 'POST':

        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            error = "Please nput csv file"
            return render(request, 'back/error.html', {'error': error})

        if csv_file.multiple_chunks():
            error = "File too large"
            return render(request, 'back/error.html', {'error': error})

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")

        for line in lines:

            fields = line.split(",")

            try:
                if len(Cat.objects.filter(name=fields[0])) == 0 and fields[0] != "Title" and fields[0] != "":
                    b = Cat(name=fields[0])
                    b.save()

            except:
                print("finish")

    return redirect('cat_list')