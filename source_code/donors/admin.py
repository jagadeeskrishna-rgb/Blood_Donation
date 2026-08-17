from django.contrib import admin
from .models import BloodDonationProfile, BloodGroup, City, District, DonationRequest, Donor, HealthStatus, OrganDonationProfile, OrganType

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ("name", "mobile_number", "blood_group", "city", "donor_type", "eligibility_status", "available")
    list_filter = ("blood_group", "city", "donor_type", "eligibility_status", "available")
    search_fields = ("name", "mobile_number", "email")

admin.site.register(BloodGroup)
admin.site.register(OrganType)
admin.site.register(City)
admin.site.register(District)
admin.site.register(HealthStatus)
admin.site.register(BloodDonationProfile)
admin.site.register(OrganDonationProfile)
admin.site.register(DonationRequest)
