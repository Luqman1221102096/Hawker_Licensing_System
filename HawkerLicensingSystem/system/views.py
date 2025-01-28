from django.shortcuts import render
from django.http import HttpResponse
managers = {"Luqman" : "1234", "Law" : "1234"}
dataAdmin = {"Long" : "1234", "Muhammad" : "1234"}
dataAdmin = {"Dan" : "1234", "Man" : "1234"}
# Create your views here.
def home(request):
    return render(request, "home.html")

def get_content(request):
    if request.method == "GET":
        name = request.GET.get('my_variable', 'Default Value')
        if(name == "Register"):
            html_content = render(request, 'register.html')
        else:
            html_content = render(request, 'login.html', {"user" : name})
        return HttpResponse(html_content)

def getDashBoard(request):
    return render(request, "dashBoard.html")
    