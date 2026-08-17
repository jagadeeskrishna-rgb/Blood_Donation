from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.urls import reverse

from .services import evaluate_donor_eligibility

mobile_validator = RegexValidator(r"^[0-9]{10}$", "Enter a valid 10 digit mobile number.")

class NamedMaster(models.Model):
    name = models.CharField(max_length=80, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name

class BloodGroup(NamedMaster):
    pass

class OrganType(NamedMaster):
    pass

class City(NamedMaster):
    pass

class District(NamedMaster):
    pass

class HealthStatus(NamedMaster):
    pass

class Donor(models.Model):
    GENDER_CHOICES = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]
    DONOR_TYPE_CHOICES = [("Blood", "Blood"), ("Organ", "Organ"), ("Both", "Both")]
    ELIGIBILITY_CHOICES = [("Eligible", "Eligible"), ("Not Eligible", "Not Eligible")]

    name = models.CharField(max_length=120)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(70)])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    mobile_number = models.CharField(max_length=10, unique=True, validators=[mobile_validator])
    email = models.EmailField(blank=True)
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.PROTECT)
    donor_type = models.CharField(max_length=10, choices=DONOR_TYPE_CHOICES)
    health_status = models.ForeignKey(HealthStatus, on_delete=models.PROTECT, null=True, blank=True)
    available = models.BooleanField(default=True)
    eligibility_status = models.CharField(max_length=20, choices=ELIGIBILITY_CHOICES, default="Eligible")
    eligibility_reason = models.CharField(max_length=160, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["blood_group", "city", "eligibility_status"]),
            models.Index(fields=["donor_type", "eligibility_status"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.blood_group}"

    def save(self, *args, **kwargs):
        self.eligibility_status, self.eligibility_reason = evaluate_donor_eligibility(self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("donor_detail", args=[self.pk])

class BloodDonationProfile(models.Model):
    FITNESS_CHOICES = [("fit", "Fit"), ("unfit", "Unfit")]
    AVAILABILITY_CHOICES = [("available", "Available"), ("unavailable", "Unavailable")]

    donor = models.OneToOneField(Donor, related_name="blood_profile", on_delete=models.CASCADE)
    last_donation_date = models.DateField(null=True, blank=True)
    medical_fitness_status = models.CharField(max_length=10, choices=FITNESS_CHOICES, default="fit")
    availability_status = models.CharField(max_length=12, choices=AVAILABILITY_CHOICES, default="available")
    eligibility_status = models.CharField(max_length=20, default="Eligible")
    eligibility_reason = models.CharField(max_length=160, blank=True)

    def save(self, *args, **kwargs):
        self.eligibility_status, self.eligibility_reason = evaluate_donor_eligibility(self.donor, donation_kind="blood", blood_profile=self)
        super().save(*args, **kwargs)

class OrganDonationProfile(models.Model):
    AVAILABILITY_CHOICES = [("available", "Available"), ("unavailable", "Unavailable")]

    donor = models.OneToOneField(Donor, related_name="organ_profile", on_delete=models.CASCADE)
    organ_type = models.ForeignKey(OrganType, on_delete=models.PROTECT)
    consent_status = models.BooleanField(default=False)
    family_contact_name = models.CharField(max_length=120)
    family_contact_mobile = models.CharField(max_length=10, validators=[mobile_validator])
    availability_status = models.CharField(max_length=12, choices=AVAILABILITY_CHOICES, default="available")
    eligibility_status = models.CharField(max_length=20, default="Eligible")
    eligibility_reason = models.CharField(max_length=160, blank=True)

    def save(self, *args, **kwargs):
        self.eligibility_status, self.eligibility_reason = evaluate_donor_eligibility(self.donor, donation_kind="organ", organ_profile=self)
        super().save(*args, **kwargs)

class DonationRequest(models.Model):
    REQUEST_TYPE_CHOICES = [("Blood", "Blood"), ("Organ", "Organ")]
    STATUS_CHOICES = [("Pending", "Pending"), ("Processing", "Processing"), ("Completed", "Completed"), ("Cancelled", "Cancelled")]

    request_type = models.CharField(max_length=10, choices=REQUEST_TYPE_CHOICES)
    hospital_name = models.CharField(max_length=160)
    contact_person = models.CharField(max_length=120)
    contact_mobile = models.CharField(max_length=10, validators=[mobile_validator])
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.PROTECT, null=True, blank=True)
    organ_type = models.ForeignKey(OrganType, on_delete=models.PROTECT, null=True, blank=True)
    emergency = models.BooleanField(default=False)
    required_date = models.DateField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="Pending")
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-emergency", "required_date", "-created_at"]

    def __str__(self):
        return f"{self.request_type} request - {self.hospital_name}"

    def matching_donors(self):
        qs = Donor.objects.filter(city=self.city, eligibility_status="Eligible", available=True)
        if self.request_type == "Blood" and self.blood_group_id:
            return qs.filter(donor_type__in=["Blood", "Both"], blood_group=self.blood_group)
        if self.request_type == "Organ" and self.organ_type_id:
            return qs.filter(donor_type__in=["Organ", "Both"], organ_profile__organ_type=self.organ_type, organ_profile__consent_status=True)
        return qs.none()
