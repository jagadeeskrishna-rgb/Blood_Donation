from django import forms
from .models import BloodDonationProfile, DonationRequest, Donor, OrganDonationProfile

class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "form-check-input" if isinstance(field.widget, forms.CheckboxInput) else "form-control"
            field.widget.attrs.setdefault("class", css)

class DonorForm(BootstrapModelForm):
    class Meta:
        model = Donor
        fields = ["name", "age", "gender", "mobile_number", "email", "address", "city", "district", "blood_group", "donor_type", "health_status", "available"]
        widgets = {"address": forms.Textarea(attrs={"rows": 3})}

class BloodDonationProfileForm(BootstrapModelForm):
    class Meta:
        model = BloodDonationProfile
        fields = ["last_donation_date", "medical_fitness_status", "availability_status"]
        widgets = {"last_donation_date": forms.DateInput(attrs={"type": "date"})}

class OrganDonationProfileForm(BootstrapModelForm):
    class Meta:
        model = OrganDonationProfile
        fields = ["organ_type", "consent_status", "family_contact_name", "family_contact_mobile", "availability_status"]

class DonationRequestForm(BootstrapModelForm):
    class Meta:
        model = DonationRequest
        fields = ["request_type", "hospital_name", "contact_person", "contact_mobile", "city", "blood_group", "organ_type", "emergency", "required_date", "status", "notes"]
        widgets = {"required_date": forms.DateInput(attrs={"type": "date"}), "notes": forms.Textarea(attrs={"rows": 3})}
