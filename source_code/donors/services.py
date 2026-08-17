ELIGIBLE = "Eligible"
NOT_ELIGIBLE = "Not Eligible"

HEALTHY_NAMES = {"fit", "healthy", "good", "normal", "medically fit"}

def donor_is_healthy(donor):
    if not donor.health_status:
        return True
    return donor.health_status.name.strip().lower() in HEALTHY_NAMES

def evaluate_donor_eligibility(donor, *, donation_kind=None, blood_profile=None, organ_profile=None):
    if donor.age > 47:
        return NOT_ELIGIBLE, "Age above 47"
    if not donor_is_healthy(donor):
        return NOT_ELIGIBLE, "Health status is not fit"
    if not donor.available:
        return NOT_ELIGIBLE, "Donor is not currently available"
    if donation_kind == "blood" and blood_profile:
        if blood_profile.medical_fitness_status == "unfit":
            return NOT_ELIGIBLE, "Blood donor is medically unfit"
        if blood_profile.availability_status == "unavailable":
            return NOT_ELIGIBLE, "Blood donor is unavailable"
    if donation_kind == "organ" and organ_profile:
        if not organ_profile.consent_status:
            return NOT_ELIGIBLE, "Organ donation consent not provided"
        if organ_profile.availability_status == "unavailable":
            return NOT_ELIGIBLE, "Organ donor is unavailable"
    return ELIGIBLE, "Basic eligibility passed"
