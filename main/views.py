from django.shortcuts import render
import json
from django.http import HttpResponse
from assistant import Assistant


def index(request):
    match request.method:
        case "POST":
            dataRequest = json.loads(request.body)
            match dataRequest:
                case {"message": {"role": str() as role, "content": str() as content}}:
                    res = Assistant(content).GetAnswer()
                    func = res.split()[0]
                    res = res.replace(func, "")
                    
                    user_info = {"role": role,
                                "content": res}
                    context = json.dumps({"message": user_info})

                    return HttpResponse(context)
        case "GET":
            return render(request, 'main/index.html')
        case _:
            print("Неподдерживаемый тип запроса")

def settings(request):
    return render(request, 'main/settings.html')

def about(request):
    return render(request, 'main/about.html')
