from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("donors/", views.donor_list, name="donor_list"),
    path("donors/add/", views.donor_create, name="donor_create"),
    path("donors/<int:pk>/", views.donor_detail, name="donor_detail"),
    path("donors/<int:pk>/edit/", views.donor_update, name="donor_update"),
    path("donors/<int:pk>/delete/", views.donor_delete, name="donor_delete"),
    path("donors/<int:pk>/blood-profile/", views.blood_profile, name="blood_profile"),
    path("donors/<int:pk>/organ-profile/", views.organ_profile, name="organ_profile"),
    path("blood-donors/", views.blood_donors, name="blood_donors"),
    path("organ-donors/", views.organ_donors, name="organ_donors"),
    path("requests/", views.request_list, name="request_list"),
    path("requests/add/", views.request_create, name="request_create"),
    path("reports/", views.reports, name="reports"),
]
