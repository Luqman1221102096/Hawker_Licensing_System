from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import getHawkers, registerHawker
currentUser = {}
# These actors have pre-existing accounts
managers = {"Luqman" : "1234", "Law" : "1234"}
dataAdmins = {"Long" : "1234", "Muhammad" : "1234"}
inspectors = {"Dan" : "1234", "Man" : "1234"}
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
    
def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    repassword = request.POST.get("rePassword")
    if password != repassword:
        return HttpResponse("Password and re-enter password do not match")
    registerHawker(username, password)
    return HttpResponse("success")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        userType = request.POST.get("userType")
        if userType == "Manager":
            for manager in managers:
                if username == manager and password == managers[manager]:
                    currentUser["User"] = userType
                    return HttpResponse("success")
            return HttpResponse("Invalid username or password", status=400)  # Send error message
        elif userType == "Inspector":
            for inspector in inspectors:
                if username == inspector and password == inspectors[inspector]:
                    currentUser["User"] = userType
                    return HttpResponse("success")
            return HttpResponse("Invalid username or password", status=400)  # Send error message
        elif userType == "DataAdmin":
            for dataAdmin in dataAdmins:
                if username == dataAdmin and password == dataAdmins[dataAdmin]:
                    currentUser["User"] = userType
                    return HttpResponse("success")
            return HttpResponse("Invalid username or password", status=400)  # Send error message
        elif userType == "Hawker":
            hawkers = getHawkers()
            for hawker in hawkers:
                if username == hawker and password == hawkers[hawker]:
                    currentUser["User"] = userType
                    return HttpResponse("success")
            return HttpResponse("Invalid username or password", status=400)  # Send error message

    return HttpResponse("Only POST requests allowed", status=405)

def dashBoard(request):
    if request.method == "GET":
        return render(request, 'dashBoard.html', {"user" : currentUser["User"]})

