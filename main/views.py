from django.shortcuts import render
from ipware import get_client_ip
import json
from django.http import HttpResponse
from ChatBot.hedgehog import Hedgehog


def index(request):
    match request.method:
        case "POST":
            dataRequest = json.loads(request.body)
            match dataRequest:
                case {"message": {"role": str() as role, "content": str() as content}}:
                    params = {"ip_client": get_client_ip(request)[0]}
                    res = Hedgehog(content, params).get_answer()
                    user_info = {"role": role, "content": res}
                    context = json.dumps({"message": user_info})

                    return HttpResponse(context)
        case "GET":
            return render(request, 'main/index.html')
        case _:
            print("<неподдерживаемый тип запроса>")

def settings(request):
    return render(request, 'main/settings.html')

def about(request):
    return render(request, 'main/about.html')
