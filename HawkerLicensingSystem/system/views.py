from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .models import registerHawker
from .forms import HawkerLicenseForm, DocumentUploadForm
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
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        repassword = request.POST.get("rePassword")
        
        if password != repassword:
            return HttpResponse("Password and re-enter password do not match", status=400)
        
        # Register the Hawker (this should add the hawker to your model/database)
        registerHawker(username, password)
        return HttpResponse("success")
    return HttpResponse("Only POST requests allowed", status=405)

def read_hawker_credentials():
    hawker_credentials = {}
    try:
        with open('hawkerList.txt', 'r') as file:
            for line in file.readlines():
                # Strip any extra spaces or newlines and split by space
                username, password = line.strip().split()
                hawker_credentials[username] = password
    except FileNotFoundError:
        print("hawkerList.txt file not found.")
    return hawker_credentials

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        userType = request.POST.get("userType")

        # Load hawker credentials from the file
        hawker_credentials = read_hawker_credentials()

        if userType == "Manager":
            for manager in managers:
                if username == manager and password == managers[manager]:
                    request.session['user'] = {'type': 'Manager', 'username': username}
                return HttpResponse("Invalid username or password", status=400)
        elif userType == "Inspector":
            for inspector in inspectors:
                if username == inspector and password == inspectors[inspector]:
                    request.session['user'] = {'type': 'Inspector', 'username': username}
                return HttpResponse("Invalid username or password", status=400)
        elif userType == "DataAdmin":
            # Check if the Data Admin credentials match 
            for dataAdmin in dataAdmins:
                if username == dataAdmin and password == dataAdmins[dataAdmin]:
                    request.session['user'] = {'type': 'DataAdmin', 'username': username}
                    return redirect('dataAdminMenu')  # Redirect to Data Admin Menu
                return HttpResponse("Invalid username or password", status=400)
        elif userType == "Hawker":
            # Check if the hawker credentials match from the file
            if username in hawker_credentials and password == hawker_credentials[username]:
                request.session['user'] = {'type': 'Hawker', 'username': username}
                return redirect('hawker_menu')  # Redirect to Hawker Menu
            return HttpResponse("Invalid username or password", status=400)

    return HttpResponse("Only POST requests allowed", status=405)

def dashBoard(request):
    if request.method == "GET":
        if 'user' in request.session:
            return render(request, 'dashBoard.html', {"user": request.session['user']['username']})
        return redirect('login')  # Redirect if no user is logged in

def apply_license(request):
    if request.method == "POST":
        return redirect("document_verification")  # Directly redirect to the next page
    return render(request, "apply_license.html")  # Render the form page

def document_verification(request):
    if request.method == "POST":
        # Process the uploaded documents (if any)
        return redirect("success")  # Redirect to success page after submission
    return render(request, "document_verification.html")

def success(request):
    return render(request, 'success.html')

def hawker_menu(request):
    if 'user' in request.session and request.session['user']['type'] == 'Hawker':
        return render(request, "hawkerMenu.html")  # Ensure this template exists
    return redirect('login')  # Redirect to login if no user is logged in


def logout_view(request):
    if 'user' in request.session:
        del request.session['user']  # Clear the user session explicitly
    return redirect('home')  # Redirect to login page after logging out

def check_status(request):
    if request.method == "POST":
        return redirect("renew_license")  # Directly redirect to the next page
    return render(request, "check_status.html")

def renew_license(request):
    if request.method == "POST":
        return redirect("payment")  # Directly redirect to the next page
    return render(request, "renew_license.html")

def payment(request):
    if request.method == "POST":
        return redirect("pay_success")  # Directly redirect to the next page
    return render(request, 'payment.html')

def pay_success(request):
    return render(request, 'pay_success.html')

def dataAdminMenu(request):
    if 'user' in request.session and request.session['user']['type'] == 'DataAdmin':
        return render(request, "dataAdminMenu.html")  # Ensure this template exists
    return redirect('login')  # Redirect to login if no user is logged in

def view_form(request):
    return render(request, "view_form.html")  # Render the form page

def checking_page(request):
    if request.method == "POST":
        return redirect("checking_detail")  # Directly redirect to the next page
    return render(request, 'checking_page.html')

def checking_detail(request):
    if request.method == "POST":
        return redirect("submit_checking")  # Directly redirect to the next page
    return render(request, "checking_detail.html")  # Render the form page

def submit_checking(request):
    return render(request, 'submit_checking.html')

def fee_status(request):
    return render(request, 'fee_status.html')

def view_history(request):
    return render(request, 'view_history.html')