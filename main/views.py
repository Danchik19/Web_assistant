from django.shortcuts import render
import json
from django.http import HttpResponse
import assistant

def index(request):
    if request.method == "POST":
        dataRequest = json.loads(request.body)
        data = dataRequest["messages"][0]
        message = data["content"]

        res = assistant.main(message)
        func = res.split()[0]
        res = res.replace(func, "")
        
        user_info = {"role": data["role"],
                     "content": res}
        context = json.dumps({"messages": [user_info]})

        return HttpResponse(context)
    
    elif request.method == "GET":
        return render(request, 'main/index.html')


def settings(request):
    return render(request, 'main/settings.html')


def about(request):
    return render(request, 'main/about.html')
