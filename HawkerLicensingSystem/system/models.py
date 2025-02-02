from django.db import models
# To read textfiles
import os
from django.conf import settings

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
