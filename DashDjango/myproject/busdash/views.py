from django.shortcuts import render

def busdash(request):
    return render(request, 'bus_template.html')
