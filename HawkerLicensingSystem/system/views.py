from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
from django import template
from .forms import *
register = template.Library()

@register.filter
def zip_lists(a, b):
    return zip(a, b)

currentUser = {}
interact = ''
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
        return JsonResponse({"status": "error", "message": "Password and re-enter password do not match"})

    registerHawker(username, password)
    request.session['user'] = {'type': 'Hawker', 'username': username}

    return JsonResponse({"status": "success", "redirect": "/hawker-menu/"})

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
    global currentUser
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
                    currentUser["User"] = userType
                    return JsonResponse({"status": "success", "menu": "managerMenu"})
            return JsonResponse({"error": "Invalid username or password"}, status=400)  # Send error message
        elif userType == "Inspector":
            for inspector in inspectors:
                if username == inspector and password == inspectors[inspector]:
                    request.session['user'] = {'type': 'Inspector', 'username': username}
                    currentUser["User"] = userType
                    return JsonResponse({"status": "success", "menu": "inspectorMenu"})
            return JsonResponse({"error": "Invalid username or password"}, status=400)  # Send error message
        elif userType == "DataAdmin":
            for dataAdmin in dataAdmins:
                if username == dataAdmin and password == dataAdmins[dataAdmin]:
                    request.session['user'] = {'type': 'DataAdmin', 'username': username}
                    currentUser["User"] = userType
                    return JsonResponse({"status": "success", "menu": "dataAdminMenu"})  # Redirect to Data Admin Menu
            return JsonResponse({"error": "Invalid username or password"}, status=400)  # Send error message
        elif userType == "Hawker":
            hawkers = getHawkers()
            if username in hawker_credentials and password == hawker_credentials[username]:
                request.session['user'] = {'type': 'Hawker', 'username': username}
                currentUser["User"] = userType
                return JsonResponse({"status": "success", "menu": "hawkerMenu"})  # Redirect to Hawker Menu
            return JsonResponse({"error": "Invalid username or password"}, status=400)  # Send error message

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)

def dashBoard(request):
    global currentUser
    if request.method == "GET":
        username = request.session.get('user', {}).get('type')
        return render(request, 'dashBoard.html', {"user" : username})
    
def viewLicense(request):
    licenseList = getAllLicenses()
    return render(request, "viewLicense.html", {"licenseList" : licenseList})

def revokeLicense(request):
    licenseList = getAllLicenses()
    return render(request, "revokeLicense.html", {"licenseList" : licenseList})

def licensePage(request, key_id):
    info = getLicenseInfo(key_id)
    return render(request, "licensePage.html", {"info" : info})

def storeReport(request, key_id):
    if request.method == "POST":
        reportText = request.POST.get("name")
        reportImage = request.FILES.get('file')
        if reportImage:  # Only insert if an image was uploaded
            insertReport(reportText, reportImage, key_id)
        else:
            return HttpResponse("Error: No image uploaded", status=400)
        form = ReportFileForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)  # Don't save yet
            report.route = f"Reports/{key_id}/"  # Pass a dynamic value
            report.save()  # Now save
    return HttpResponse("success")

def note(request, key_id):
    info = getLicenseInfo(key_id)
    return render(request, "note.html", {"info" : info})

def storeNote(request, key_id):
    if request.method == "POST":
        reportText = request.POST.get("reportText")
        insertNote(reportText, key_id)
    return redirect("revokeLicense")

def revokeRequests(request):
    licenseList = getAllLicenses()
    return render(request, "revokeRequests.html", {"licenseList" : licenseList})

def revokeApproval(request, key_id):
    global interact
    if request.method == 'POST':
        if key_id == "0":
            updateLicense(interact, "Approved Revoke")
        elif key_id == "-1":
            updateLicense(interact, "Active")
        key_id = ''
        return HttpResponse("success")
    else:
        interact = key_id
        info = ReportFile.objects.filter(route=f"Reports/{key_id}/").latest('uploaded_at')
        return render(request, "revokeApproval.html", {"info" : info})
    
def viewFormManager(request):
    licenses = getAllLicenses()
    return render(request, "viewFormManager.html", {"licenses" : licenses})

def viewValidated(request):
    licenses = getAllLicenses()
    return render(request, "viewValidated.html", {"licenses" : licenses})

def applicationApproval(request):
    if request.method == 'POST':
        operation = request.POST.get("operation")
        id = request.POST.get("id")
        if operation == "0":
            updateLicense(id, "Active")
        elif operation == "-1":
            updateLicense(id, "Rejected")
        return redirect("viewValidated")
    id = request.GET.get("id")
    text = getAdminReport(id)
    info = getLicenseInfo(id)
    return render(request, "applicationApproval.html", {"text" : text, "info" : info})

# Long
def apply_license(request):
    global interact
    if request.method == "POST":
        owner = request.POST.get("name")
        location = request.POST.get("stall_location")
        date = request.POST.get("start_date")
        id = addLicense(owner, location, date)
        interact = id
        return redirect("document_verification")  # Directly redirect to the next page
    return render(request, "apply_license.html")  # Render the form page

def document_verification(request):
    if request.method == "POST":
        # Process the uploaded documents (if any)
        identity_proof = request.FILES.get("identity_proof")
        business_registration = request.FILES.get("business_registration")
        health_certificate = request.FILES.get("health_certificate")
        location_permit = request.FILES.get("location_permit")

        # Ensure all required files are uploaded
        if not all([identity_proof, business_registration, health_certificate, location_permit]):
            return HttpResponse("Error: All documents are required", status=400)

        # Save each file as a separate entry in the database
        ReportFile.objects.create(name="Identity Proof", route=f"Documents/{interact}/", file=identity_proof)
        ReportFile.objects.create(name="Business Registration", route=f"Documents/{interact}/", file=business_registration)
        ReportFile.objects.create(name="Health Certificate", route=f"Documents/{interact}/", file=health_certificate)
        ReportFile.objects.create(name="Location Permit", route=f"Documents/{interact}/", file=location_permit)
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
    licenses = getAllLicenses()
    username = request.session.get('user', {}).get('username')
    return render(request, "check_status.html", {"licenses" : licenses, "username" : username})

def renew_license(request):
    if request.method == "POST":
        return redirect("payment")  # Directly redirect to the next page
    licenses = getAllLicenses()
    username = request.session.get('user', {}).get('username')
    return render(request, "renew_license.html", {"licenses" : licenses, "username" : username})

def payment(request):
    global intract
    if request.method == "POST":
        return redirect("pay_success")  # Directly redirect to the next page
    licenses = getAllLicenses()
    username = request.session.get('user', {}).get('username')
    return render(request, 'payment.html', {"licenses" : licenses, "username" : username})

def pay_success(request):
    licenses = getAllLicenses()
    username = request.session.get('user', {}).get('username')
    for license in licenses:
        if license.owner == username and license.status == "Expired":
            updateLicense(license.id, "Active")
    return render(request, 'pay_success.html')

def dataAdminMenu(request):
    if 'user' in request.session and request.session['user']['type'] == 'DataAdmin':
        return render(request, "dataAdminMenu.html")  # Ensure this template exists
    return redirect('login')  # Redirect to login if no user is logged in

def view_form(request):
    if request.method == "POST":
        id = request.POST.get("id")
        if request.POST.get("valid") == "valid":
            updateLicense(id, "Valid")
        else:
            updateLicense(id, "Invalid")
    licenseList = getAllLicenses()
    return render(request, "view_form.html", {"licenseList" : licenseList})  # Render the form page

def checking_page(request):
    if request.method == "POST":
        return redirect("checking_detail")  # Directly redirect to the next page
    licenseList = getAllLicenses()
    return render(request, 'checking_page.html', {"licenseList" : licenseList})

def checking_detail(request):
    if request.method == "POST":
        text = request.POST.get("comments", "No data")
        c1 = request.POST.get("criteria1", 'No')
        c2 = request.POST.get("criteria2", 'No')
        c3 = request.POST.get("criteria3", 'No')
        c4 = request.POST.get("criteria4", 'No')
        id = request.POST.get("id")
        insertAdmin(text, c1, c2, c3, c4, id)
        return redirect("submit_checking")  # Directly redirect to the next page
    id = request.GET.get("id")
    files = ReportFile.objects.filter(route=f"Documents/{id}/").order_by('-uploaded_at')[:4]
    return render(request, "checking_detail.html", {"files" : files, "id" : id})  # Render the form page)

def submit_checking(request):
    return render(request, 'submit_checking.html')

def fee_status(request):
    if request.method == "POST":
        updateLicense(request.POST.get("id"), "Bar")
        redirect("fee_status")
    licenses = getAllLicenses()
    return render(request, 'fee_status.html', {"licenses" : licenses})

def view_history(request):
    licenses = getAllLicenses()
    return render(request, 'view_history.html', {"licenses" : licenses})