from django.db import models
# To read textfiles
import os
from django.conf import settings
from dataclasses import dataclass
from django.core.files.storage import FileSystemStorage
# Struct for license information
@dataclass
class licenseInfo:
    id: str = ""
    owner: str = ""
    status: str = ""
    date: str = ""
    location: str = ""

def report_upload_path(instance, filename):
    return f"{instance.route}{filename}"

class ReportFile(models.Model):
    name = models.CharField(max_length=255, default="Untitled")
    route = models.CharField(max_length=255, default='Reports/')
    file = models.FileField(upload_to=report_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Create your models here.
def getHawkers():
    hawkers = {}
    f = open(os.path.join(settings.BASE_DIR, "hawkerList.txt"), "r")
    name = ""
    password = ""
    for line in f:
        name = ""
        password = ""
        for i in range(len(line)):
            if line[i] == " ":
                name = line[:i]
                password = line[i+1:len(line)-1]
                break
        hawkers[name] = password
    f.close()
    return hawkers

def registerHawker(name, password):
    # Create file if it does not exist
    f = open(os.path.join(settings.BASE_DIR, "hawkerList.txt"), "a")
    f.write(f"{name} {password}\n")
    f.close()

def parse_license_info(data: str) -> licenseInfo:
    fields = data.split(":")  # Split string by ':'
    return licenseInfo(*fields)  # Unpack fields into the dataclass

def getLicenseInfo(wantedId):
    f = open(os.path.join(settings.BASE_DIR, "licenseList.txt"), "r")
    li = licenseInfo()
    id = ""
    for line in f:
        for i in range(len(line)):
            if line[i] == ":":
                id = line[:i]
                if wantedId == id:
                    li = parse_license_info(line)
                    break
    f.close()
    return li
            
def getAllLicenses():
    f = open(os.path.join(settings.BASE_DIR, "licenseList.txt"), "r")
    licenseList = []
    for line in f:
        licenseList.append(parse_license_info(line))
    f.close()
    return licenseList

def insertReport(reportText, reportImage, key_id):
    # clears folder
    if os.path.exists(f"media/Reports/{key_id}"):
        for file in os.listdir(f"media/Reports/{key_id}"):
            file_path = os.path.join(f"media/Reports/{key_id}", file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)  # Delete file
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    #Adds new content
    try:
        os.mkdir(f"media/Reports/{key_id}")
        f = open(os.path.join(settings.BASE_DIR, f"media/Reports/{key_id}/report.txt"), "w")
        f.write(reportText)
    except FileExistsError:
        f = open(os.path.join(settings.BASE_DIR, f"media/Reports/{key_id}/report.txt"), "w")
        f.write(reportText)
    #fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, f"media/Reports/{key_id}"))
    #filename = fs.save(reportImage.name, reportImage)
    f.close()
    updateLicense(key_id, "Pending")

def insertNote(reportText, key_id):
    # clears folder
    if os.path.exists(f"media/Notes/{key_id}"):
        for file in os.listdir(f"media/Notes/{key_id}"):
            file_path = os.path.join(f"media/Notes/{key_id}", file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)  # Delete file
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    #Adds new content
    try:
        os.mkdir(f"media/Notes/{key_id}")
        f = open(os.path.join(settings.BASE_DIR, f"media/Notes/{key_id}/report.txt"), "w")
        f.write(reportText)
    except FileExistsError:
        f = open(os.path.join(settings.BASE_DIR, f"media/Notes/{key_id}/report.txt"), "w")
        f.write(reportText)
    f.close()
    updateLicense(key_id, "Revoke")

def updateLicense(key_id, newStatus):
    licenseList = getAllLicenses()
    for license in licenseList:
        if license.id == key_id:
            license.status = newStatus
            break
    #open(os.path.join(settings.BASE_DIR, "licenseList.txt"), "w").close()#clear file
    f = open(os.path.join(settings.BASE_DIR, "licenseList.txt"), "w")
    for license in licenseList:
        f.write(f"{license.id}:{license.owner}:{license.status}:{license.date}:{license.location}")
    f.close()

def getReport(key_id):
    if os.path.exists(f"Reports/{key_id}"):
        f = open(os.path.join(settings.BASE_DIR, f"Reports/{key_id}/report.txt"), "r")
