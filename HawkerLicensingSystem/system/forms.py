from django import forms
from .models import *

class ReportFileForm(forms.ModelForm):
    class Meta:
        model = ReportFile
        fields = ['name', 'file']