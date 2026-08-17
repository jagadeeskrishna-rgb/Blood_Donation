from datetime import date, timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import BloodDonationProfile, BloodGroup, City, District, DonationRequest, Donor, HealthStatus, OrganDonationProfile, OrganType

class DonorWorkflowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("staff", password="pass12345")
        self.city = City.objects.create(name="Chennai")
        self.district = District.objects.create(name="Chennai")
        self.bg = BloodGroup.objects.create(name="O+")
        self.organ = OrganType.objects.create(name="Kidney")
        self.fit = HealthStatus.objects.create(name="Fit")
        self.unfit = HealthStatus.objects.create(name="Unfit")

    def donor(self, **overrides):
        data = dict(name="Academic Donor", age=30, gender="Male", mobile_number="9876543210", address="Demo Street", city=self.city, district=self.district, blood_group=self.bg, donor_type="Both", health_status=self.fit, available=True)
        data.update(overrides)
        return Donor.objects.create(**data)

    def test_age_above_47_is_not_eligible(self):
        donor = self.donor(age=48)
        self.assertEqual(donor.eligibility_status, "Not Eligible")
        self.assertEqual(donor.eligibility_reason, "Age above 47")

    def test_basic_eligible_donor_passes(self):
        donor = self.donor()
        self.assertEqual(donor.eligibility_status, "Eligible")
        self.assertEqual(donor.eligibility_reason, "Basic eligibility passed")

    def test_organ_consent_controls_organ_eligibility(self):
        donor = self.donor()
        profile = OrganDonationProfile.objects.create(donor=donor, organ_type=self.organ, consent_status=False, family_contact_name="Parent", family_contact_mobile="9876500000")
        self.assertEqual(profile.eligibility_status, "Not Eligible")
        self.assertIn("consent", profile.eligibility_reason.lower())

    def test_request_finds_matching_blood_donor(self):
        donor = self.donor()
        BloodDonationProfile.objects.create(donor=donor)
        request = DonationRequest.objects.create(request_type="Blood", hospital_name="City Hospital", contact_person="Nurse", contact_mobile="9876500001", city=self.city, blood_group=self.bg, required_date=date.today() + timedelta(days=1), created_by=self.user)
        self.assertIn(donor, request.matching_donors())

    def test_login_required_for_dashboard(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
