# Blood Donation Prediction System with Blood Donor and Organ Donor Information

## 1. Abstract

The Blood Donation Prediction System with Blood Donor and Organ Donor Information is a web-based academic project designed to help hospitals, blood banks, and healthcare organizations manage donor records in a structured and efficient way. Manual donor record maintenance is time-consuming and difficult during emergency situations because staff must search through paper records or spreadsheets to identify suitable donors.

This project provides a centralized system to store blood donor and organ donor details, check donor eligibility, and classify donors into Eligible and Not Eligible categories based on predefined academic rules. The system allows users to register donors, manage blood donor details, manage organ donor details, search donors by blood group, city, organ type, and eligibility status, and generate useful reports.

For this academic project, a simple rule-based prediction method is used. If the donor age is above 47, the donor is moved to the Not Eligible list. Other basic details such as health status, availability status, and consent status can also be used to identify donor eligibility. This system is useful for student-level learning because it covers database design, CRUD operations, authentication, search, filtering, reporting, dashboard design, and basic rule-based prediction.

## 2. Problem Statement

Hospitals and blood banks need quick access to accurate donor information, especially during emergency blood or organ requirements. In many places, donor information is still maintained manually using notebooks, files, or spreadsheets. This makes it difficult to search donors, update donor details, and identify eligible donors quickly.

The proposed system solves this problem by providing a web-based donor management and eligibility prediction system.

## 3. Existing Problem

The existing manual or spreadsheet-based donor management process has the following problems:

- Donor records are difficult to search quickly.
- Blood donor and organ donor details are not maintained in a centralized system.
- Eligibility checking is done manually.
- Staff may take more time to find suitable donors during emergencies.
- Duplicate and outdated donor records may exist.
- Reports are difficult to prepare manually.
- Donor availability status is not clearly maintained.
- Not eligible donors are not separated properly.
- Manual records have a higher risk of data loss.
- Hospital staff and blood bank staff cannot easily filter donors by blood group, city, organ type, or eligibility status.

## 4. Proposed Solution

The proposed system is a Django-based web application that stores and manages blood donor and organ donor information in a database. The application provides login-based access for admin and staff users. Donor details can be added, updated, viewed, searched, and reported through the web interface.

The system automatically checks donor eligibility using predefined academic rules. The main eligibility rule used in this project is:

> If donor age is above 47, the donor is moved to the Not Eligible list.

The system also supports additional basic checking using health status, availability status, and organ donation consent status.

The proposed system provides the following benefits:

- Centralized donor information storage.
- Easy donor registration and update process.
- Automatic eligible and not eligible classification.
- Fast donor search and filtering.
- Separate blood donor and organ donor management.
- Useful reports for hospital and blood bank staff.
- Better project demonstration for academic evaluation.

## 5. Project Objectives

- To develop a web-based donor management system.
- To store blood donor information securely.
- To store organ donor information securely.
- To classify donors into Eligible and Not Eligible lists.
- To implement age-based donor eligibility prediction.
- To allow fast donor search by blood group, city, organ type, and eligibility status.
- To generate donor-related reports.
- To demonstrate Django-based full-stack web application development.

## 6. Module Details

### 6.1 Authentication Module

The Authentication Module controls secure access to the Blood Donation Prediction System. It allows only authorized users such as administrators and staff members to use the system. Since donor information contains personal and medical-related details, login-based access is important for maintaining privacy and security.

This module provides admin login, staff login, logout, and password change options. Role-based access control is used to separate admin and staff permissions. For example, an admin may manage users and master data, while staff users may mainly handle donor registration, searching, and report viewing.

This module ensures that every user enters the system through a verified account, reducing unauthorized access and improving system reliability.

Main features:

- Admin login
- Staff login
- Logout
- Change password
- Role-based access control

### 6.2 Dashboard Module

The Dashboard Module provides a quick overview of the entire system. After login, users can view important summary information in one place without opening each section separately.

The dashboard displays total donor count, blood donor count, organ donor count, eligible donor count, not eligible donor count, and available donor count. It may also show blood group-wise summaries and organ donor summaries.

This module is useful for hospital staff and blood bank administrators because it gives instant statistical information. During emergencies, staff can quickly understand how many donors are available and how many are eligible.

Main features:

- Total donor count
- Blood donor count
- Organ donor count
- Eligible donor count
- Not eligible donor count
- Available donor count
- Blood group summary
- Organ donor summary

### 6.3 Donor Registration Module

The Donor Registration Module is used to store and manage general donor information. This is the base module of the system because both blood donors and organ donors require basic personal details.

This module allows users to add, edit, delete, and view donor records. It stores donor name, age, gender, mobile number, email address, address, city, district, blood group, and donor type. The donor type helps identify whether the person is a blood donor, organ donor, or both.

By maintaining donor information in a centralized database, this module reduces manual paperwork and makes donor record management faster and more organized.

Main features:

- Add donor
- Edit donor
- Delete donor
- View donor details
- Store contact details
- Store address details
- Store blood group and donor type

### 6.4 Blood Donor Module

The Blood Donor Module manages information related specifically to blood donation. It stores details required to identify and classify blood donors.

This module includes blood donor registration, blood group details, last donation date, medical fitness status, and availability status. It also separates donors into eligible blood donors and not eligible blood donors based on the system's prediction rules.

This module is especially useful during blood requirement situations because staff can search donors by blood group, location, and availability. It helps hospitals and blood banks identify suitable blood donors quickly.

Main features:

- Blood donor registration
- Blood group details
- Last donation date
- Medical fitness status
- Availability status
- Eligible blood donor list
- Not eligible blood donor list

### 6.5 Organ Donor Module

The Organ Donor Module manages organ donation-related information. Organ donation requires additional details such as organ type, consent status, and family contact information.

This module allows users to register organ donors, select the organ type, update consent status, and store emergency or family contact details. It also maintains eligible and not eligible organ donor lists.

Consent status is an important part of this module because organ donation depends on the donor's willingness and approval. This module helps healthcare organizations maintain structured organ donor records for academic and administrative use.

Main features:

- Organ donor registration
- Organ type selection
- Consent status
- Family contact details
- Eligible organ donor list
- Not eligible organ donor list

### 6.6 Eligibility Prediction Module

The Eligibility Prediction Module is the main logic module of the project. It checks donor information and classifies donors into Eligible and Not Eligible categories.

For this academic project, a simple rule-based prediction method is used. The main rule is: if the donor age is above 47, the donor is marked as Not Eligible. If the donor age is 47 or below, the donor may be marked as Eligible, provided other basic checks are satisfied.

This module can also check health status, availability status, and organ consent status. For example, if a donor is medically unfit, unavailable, or has not given consent for organ donation, the donor may be marked as Not Eligible.

The module also displays the reason for eligibility or rejection, such as "Age above 47" or "Basic eligibility passed." This makes the classification easy to understand during project demonstration.

Main features:

- Age validation
- Health status validation
- Availability validation
- Organ consent validation
- Automatic eligibility status update
- Eligibility reason display

Sample academic logic:

```python
if age > 47:
    eligibility_status = "Not Eligible"
    eligibility_reason = "Age above 47"
else:
    eligibility_status = "Eligible"
    eligibility_reason = "Basic eligibility passed"
```

### 6.7 Search and Filter Module

The Search and Filter Module helps users find donor records quickly from the database. In manual systems, searching donor records can take a long time, especially during emergencies. This module solves that problem by providing fast filtering options.

Users can search donors by name, mobile number, blood group, city, district, donor type, organ type, and eligibility status. For example, a staff member can search for eligible blood donors with a specific blood group in a specific city.

This module improves system usability and helps hospitals or blood banks quickly identify suitable donors.

Main features:

- Search by donor name
- Search by mobile number
- Search by blood group
- Search by city
- Search by district
- Search by donor type
- Search by organ type
- Search by eligibility status

### 6.8 Hospital / Blood Bank Request Module

The Hospital / Blood Bank Request Module is used to manage requests for blood or organ donors. Hospitals or blood banks may create requests when they need a specific blood group or organ donor.

This module allows users to create blood requests, create organ requests, search matching donors, mark emergency requests, and track request status. Request status may include pending, processing, completed, or cancelled.

This module connects donor information with real-world hospital requirements. It makes the system more practical by allowing staff to match available donors with active medical needs.

Main features:

- Create blood request
- Create organ request
- Search matching donors
- Emergency request marking
- Request status tracking

### 6.9 Reports Module

The Reports Module generates useful donor-related reports. Reports help administrators and staff analyze donor data and present project output clearly.

This module can generate total donor reports, blood donor reports, organ donor reports, eligible donor reports, not eligible donor reports, blood group-wise reports, city-wise reports, and organ type-wise reports.

The system may also provide Excel export and PDF export options. These reports are useful for academic evaluation because they show how data is stored, filtered, classified, and presented in a structured format.

Main features:

- Total donor report
- Blood donor report
- Organ donor report
- Eligible donor report
- Not eligible donor report
- Blood group-wise report
- City-wise report
- Organ type-wise report
- Excel export
- PDF export

### 6.10 Admin Settings Module

The Admin Settings Module allows the administrator to manage system-level information. This module is mainly used for maintaining master data and user accounts.

The admin can manage users, blood groups, organ types, cities, districts, and health status values. For example, if a new organ type or city needs to be added, the admin can update it through this module.

This module improves flexibility because important dropdown values and system users can be managed without changing the program code. It helps keep the system organized and easy to maintain.

Main features:

- Manage users
- Manage blood groups
- Manage organ types
- Manage cities and districts
- Manage health status values
