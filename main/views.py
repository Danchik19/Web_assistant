from django.shortcuts import render


def func_main(request):
    return render(request, 'main/func_main.html')

def func_settings(request):
    return render(request, 'main/func_settings.html')

def func_opportunities(request):
    return render(request, 'main/func_opportunities.html')