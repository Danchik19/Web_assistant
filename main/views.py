from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')

def settings(request):
    return render(request, 'main/settings.html')

def about(request):
    return render(request, 'main/about.html')