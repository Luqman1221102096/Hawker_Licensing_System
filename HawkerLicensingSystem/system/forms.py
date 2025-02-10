from django import forms

class HawkerLicenseForm(forms.Form):
    full_name = forms.CharField(label="Full Name", max_length=100, required=True)
    identification_number = forms.CharField(label="Identification Number", max_length=20, required=True)
    contact_information = forms.CharField(label="Contact Information", max_length=50, required=True)
    business_name = forms.CharField(label="Business Name", max_length=100, required=True)
    stall_location = forms.CharField(label="Stall Location", max_length=100, required=True)
    type_of_business = forms.ChoiceField(
        label="Type of Business",
        choices=[
            ("food", "Food"),
            ("retail", "Retail"),
            ("services", "Services"),
        ],
        required=True
    )
    license_type = forms.ChoiceField(
        label="License Type",
        choices=[
            ("temporary", "Temporary"),
            ("permanent", "Permanent"),
        ],
        required=True
    )
    start_date = forms.DateField(label="Start Date", widget=forms.DateInput(attrs={"type": "date"}), required=True)
    previous_license = forms.CharField(label="Previous License (Optional)", max_length=50, required=False)
    other_permit = forms.CharField(label="Other Permit (Optional)", max_length=50, required=False)

class DocumentUploadForm(forms.Form):
    proof_of_identity = forms.FileField(label="Proof of Identity (e.g., Passport, ID Card)", required=True)
    business_registration = forms.FileField(label="Business Registration Document", required=True)
    health_certificate = forms.FileField(label="Health Certificate", required=True)
    location_zoning = forms.FileField(label="Location/Zoning Approval", required=True)
