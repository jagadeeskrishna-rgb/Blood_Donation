import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BloodDonationProfileForm, DonationRequestForm, DonorForm, OrganDonationProfileForm
from .models import BloodDonationProfile, BloodGroup, City, DonationRequest, Donor, OrganDonationProfile, OrganType

def is_admin(user):
    return user.is_superuser or user.groups.filter(name="Administrator").exists()

def donor_queryset(request):
    qs = Donor.objects.select_related("city", "district", "blood_group", "health_status")
    search = request.GET.get("q", "").strip()
    if search:
        qs = qs.filter(Q(name__icontains=search) | Q(mobile_number__icontains=search) | Q(email__icontains=search))
    for field in ["blood_group", "city", "district", "donor_type", "eligibility_status"]:
        value = request.GET.get(field)
        if value:
            qs = qs.filter(**{field: value})
    organ_type = request.GET.get("organ_type")
    if organ_type:
        qs = qs.filter(organ_profile__organ_type_id=organ_type)
    return qs

@login_required
def dashboard(request):
    donors = Donor.objects.all()
    context = {
        "total_donors": donors.count(),
        "blood_donors": donors.filter(donor_type__in=["Blood", "Both"]).count(),
        "organ_donors": donors.filter(donor_type__in=["Organ", "Both"]).count(),
        "eligible_donors": donors.filter(eligibility_status="Eligible").count(),
        "not_eligible_donors": donors.filter(eligibility_status="Not Eligible").count(),
        "available_donors": donors.filter(available=True).count(),
        "blood_summary": BloodGroup.objects.annotate(total=Count("donor")),
        "organ_summary": OrganType.objects.annotate(total=Count("organdonationprofile")),
        "recent_requests": DonationRequest.objects.select_related("city", "blood_group", "organ_type")[:5],
    }
    return render(request, "donors/dashboard.html", context)

@login_required
def donor_list(request):
    context = {
        "donors": donor_queryset(request),
        "blood_groups": BloodGroup.objects.all(),
        "cities": City.objects.all(),
        "organ_types": OrganType.objects.all(),
    }
    return render(request, "donors/donor_list.html", context)

@login_required
def donor_detail(request, pk):
    return render(request, "donors/donor_detail.html", {"donor": get_object_or_404(Donor, pk=pk)})

@login_required
def donor_create(request):
    form = DonorForm(request.POST or None)
    if form.is_valid():
        donor = form.save(commit=False)
        donor.created_by = request.user
        donor.save()
        messages.success(request, "Donor registered successfully.")
        return redirect(donor)
    return render(request, "donors/form.html", {"form": form, "title": "Register Donor"})

@login_required
def donor_update(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    form = DonorForm(request.POST or None, instance=donor)
    if form.is_valid():
        form.save()
        messages.success(request, "Donor updated successfully.")
        return redirect(donor)
    return render(request, "donors/form.html", {"form": form, "title": "Update Donor"})

@login_required
@user_passes_test(is_admin)
def donor_delete(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == "POST":
        donor.delete()
        messages.success(request, "Donor deleted.")
        return redirect("donor_list")
    return render(request, "donors/confirm_delete.html", {"object": donor, "title": "Delete Donor"})

@login_required
def blood_profile(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    profile = getattr(donor, "blood_profile", None)
    form = BloodDonationProfileForm(request.POST or None, instance=profile)
    if form.is_valid():
        item = form.save(commit=False)
        item.donor = donor
        item.save()
        messages.success(request, "Blood donor profile saved.")
        return redirect(donor)
    return render(request, "donors/form.html", {"form": form, "title": f"Blood Profile - {donor.name}"})

@login_required
def organ_profile(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    profile = getattr(donor, "organ_profile", None)
    form = OrganDonationProfileForm(request.POST or None, instance=profile)
    if form.is_valid():
        item = form.save(commit=False)
        item.donor = donor
        item.save()
        messages.success(request, "Organ donor profile saved.")
        return redirect(donor)
    return render(request, "donors/form.html", {"form": form, "title": f"Organ Profile - {donor.name}"})

@login_required
def blood_donors(request):
    donors = donor_queryset(request).filter(donor_type__in=["Blood", "Both"])
    return render(request, "donors/donor_list.html", {"donors": donors, "page_title": "Blood Donors", "blood_groups": BloodGroup.objects.all(), "cities": City.objects.all(), "organ_types": OrganType.objects.all()})

@login_required
def organ_donors(request):
    donors = donor_queryset(request).filter(donor_type__in=["Organ", "Both"])
    return render(request, "donors/donor_list.html", {"donors": donors, "page_title": "Organ Donors", "blood_groups": BloodGroup.objects.all(), "cities": City.objects.all(), "organ_types": OrganType.objects.all()})

@login_required
def request_list(request):
    return render(request, "donors/request_list.html", {"requests": DonationRequest.objects.select_related("city", "blood_group", "organ_type")})

@login_required
def request_create(request):
    form = DonationRequestForm(request.POST or None)
    if form.is_valid():
        item = form.save(commit=False)
        item.created_by = request.user
        item.save()
        messages.success(request, "Request saved.")
        return redirect("request_list")
    return render(request, "donors/form.html", {"form": form, "title": "Create Request"})

@login_required
def reports(request):
    donors = donor_queryset(request)
    if request.GET.get("export") == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="donor-report.csv"'
        writer = csv.writer(response)
        writer.writerow(["Name", "Mobile", "Blood Group", "City", "Donor Type", "Eligibility", "Reason"])
        for donor in donors:
            writer.writerow([donor.name, donor.mobile_number, donor.blood_group, donor.city, donor.donor_type, donor.eligibility_status, donor.eligibility_reason])
        return response
    return render(request, "donors/reports.html", {"donors": donors, "blood_groups": BloodGroup.objects.all(), "cities": City.objects.all(), "organ_types": OrganType.objects.all()})
