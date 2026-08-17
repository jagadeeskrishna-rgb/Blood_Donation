from datetime import date, timedelta
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from donors.models import BloodDonationProfile, BloodGroup, City, District, Donor, HealthStatus, OrganDonationProfile, OrganType

class Command(BaseCommand):
    help = "Load academic demo master data and sample donors."

    def handle(self, *args, **options):
        admin_group, _ = Group.objects.get_or_create(name="Administrator")
        staff_group, _ = Group.objects.get_or_create(name="Staff")
        staff, _ = User.objects.get_or_create(username="staff", defaults={"is_staff": True})
        staff.set_password("staff12345")
        staff.groups.add(staff_group)
        staff.save()
        blood_groups = [BloodGroup.objects.get_or_create(name=x)[0] for x in ["A+", "B+", "O+", "AB+", "A-", "O-"]]
        organs = [OrganType.objects.get_or_create(name=x)[0] for x in ["Kidney", "Liver", "Heart", "Eye"]]
        city = City.objects.get_or_create(name="Chennai")[0]
        district = District.objects.get_or_create(name="Chennai")[0]
        fit = HealthStatus.objects.get_or_create(name="Fit")[0]
        unfit = HealthStatus.objects.get_or_create(name="Unfit")[0]
        samples = [
            ("Arun Kumar", 32, "Male", "9000000001", "Blood", blood_groups[2], fit, True),
            ("Meena Ravi", 45, "Female", "9000000002", "Both", blood_groups[0], fit, True),
            ("Joseph Raj", 52, "Male", "9000000003", "Organ", blood_groups[1], fit, True),
            ("Nisha Priya", 28, "Female", "9000000004", "Blood", blood_groups[3], unfit, True),
        ]
        for name, age, gender, mobile, donor_type, bg, health, available in samples:
            donor, _ = Donor.objects.get_or_create(mobile_number=mobile, defaults={"name": name, "age": age, "gender": gender, "address": "Academic sample address", "city": city, "district": district, "blood_group": bg, "donor_type": donor_type, "health_status": health, "available": available, "created_by": staff})
            if donor_type in ["Blood", "Both"]:
                BloodDonationProfile.objects.get_or_create(donor=donor, defaults={"last_donation_date": date.today() - timedelta(days=120)})
            if donor_type in ["Organ", "Both"]:
                OrganDonationProfile.objects.get_or_create(donor=donor, defaults={"organ_type": organs[0], "consent_status": donor.age <= 47, "family_contact_name": "Family Member", "family_contact_mobile": "9111111111"})
        self.stdout.write(self.style.SUCCESS("Demo data loaded. Staff login: staff / staff12345"))
