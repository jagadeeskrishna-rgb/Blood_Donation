# Blood Donation Prediction System with Blood Donor and Organ Donor Information

This package contains a complete academic Django web application for managing blood donors, organ donors, donor eligibility prediction, hospital or blood bank requests, search/filtering, and reports.

## Technology
- Backend: Django 5.2
- Frontend: HTML, CSS, Bootstrap 5
- Database: SQLite
- Testing: Django TestCase

## Quick Start
```powershell
cd source_code
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo_data
python manage.py runserver
```

Open http://127.0.0.1:8000/. Demo staff login after seeding: `staff` / `staff12345`.

## Academic Rule
If donor age is above 47, the donor is classified as Not Eligible. Additional checks reject unfit, unavailable, or non-consenting organ donors.
