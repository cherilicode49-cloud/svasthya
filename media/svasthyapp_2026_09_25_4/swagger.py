import re
from rest_framework import permissions
# pyrefly: ignore [missing-import]
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from django.urls import get_resolver
from django.http import JsonResponse


# Parameter schemas catalog for known endpoint patterns
ENDPOINT_METADATA = {
    # Auth & Admin
    'admin_login': {
        'tag': 'Authentication',
        'method': 'POST',
        'summary': 'Admin Login',
        'description': 'Authenticate admin/staff user with email and password.',
        'params': {
            'email': ('string', 'User email address', 'admin@svasthya.com', True),
            'password': ('string', 'User password', '********', True),
        }
    },
    'send_otp': {
        'tag': 'Authentication',
        'method': 'POST',
        'summary': 'Send OTP',
        'description': 'Send OTP to mobile or email for verification.',
        'params': {
            'mobile': ('string', 'Mobile phone number', '9876543210', False),
            'email': ('string', 'Email address', 'user@example.com', False),
        }
    },
    'verify_otp': {
        'tag': 'Authentication',
        'method': 'POST',
        'summary': 'Verify OTP',
        'description': 'Verify received OTP code.',
        'params': {
            'mobile': ('string', 'Mobile phone number', '9876543210', False),
            'email': ('string', 'Email address', 'user@example.com', False),
            'otp': ('string', 'OTP code received', '123456', True),
        }
    },

    # Appointments
    'appointment_create': {
        'tag': 'Appointments',
        'method': 'POST',
        'summary': 'Create Employee/Individual Appointment',
        'description': 'Create a new appointment with package, center, dates, and payment options.',
        'params': {
            'employee': ('integer', 'Employee ID (for employee appointments)', 1, False),
            'individual': ('integer', 'Individual user ID (for individual appointments)', 1, False),
            'patient': ('integer', 'Dependent Patient ID if applicable', 1, False),
            'package': ('integer', 'Package ID', 10, True),
            'center': ('integer', 'Center ID', 5, False),
            'appointment_date_1': ('string', 'Preferred health checkup date 1 (YYYY-MM-DD)', '2026-10-01', False),
            'appointment_date_2': ('string', 'Preferred health checkup date 2 (YYYY-MM-DD)', '2026-10-02', False),
            'home_sample_date_1': ('string', 'Preferred home sample date 1 (YYYY-MM-DD)', '2026-10-01', False),
            'home_sample_date_2': ('string', 'Preferred home sample date 2 (YYYY-MM-DD)', '2026-10-02', False),
            'flag': ('string', 'employee or individual', 'employee', False),
            'cart_flag': ('string', 'cart flag indicator', 'yes/no', False),
            'is_payment': ('string', 'Payment status or flag', 'true', False),
            'method': ('string', 'Payment method (Online / Cash / Corporate)', 'Online', False),
            'transaction_id': ('string', 'Payment transaction ID', 'TXN123456', False),
        }
    },
    'appointment_booking_reschedule': {
        'tag': 'Appointments',
        'method': 'POST',
        'summary': 'Confirm Slot or Reschedule Appointment',
        'description': 'Confirm appointment date or reschedule appointment and log audit record.',
        'params': {
            'appointment': ('integer', 'Appointment ID', 1, True),
            'status': ('string', 'Confirmed | Rescheduled', 'Confirmed', True),
            'confirm_appointment_date': ('string', 'Confirmed checkup date (YYYY-MM-DD)', '2026-10-05', False),
            'confirm_home_sample_date': ('string', 'Confirmed home sample date (YYYY-MM-DD)', '2026-10-05', False),
            'new_appointment_date': ('string', 'New checkup date if rescheduling', '2026-10-05', False),
            'new_home_sample_date': ('string', 'New home sample date if rescheduling', '2026-10-05', False),
            'center': ('integer', 'Center ID', 5, False),
            'rescheduled_by': ('string', 'Staff name or role', 'Staff', False),
            'reason': ('string', 'Reason for reschedule', 'Slot unavailable', False),
            'remark': ('string', 'Staff remarks', 'Slot confirmed for 10 AM', False),
        }
    },
    'appointment_reschedule': {
        'tag': 'Appointments',
        'method': 'POST',
        'summary': 'Reschedule Appointment (Alias)',
        'description': 'Reschedule existing appointment with new dates.',
        'params': {
            'appointment_id': ('integer', 'Appointment ID', 1, True),
            'new_appointment_date': ('string', 'New checkup date (YYYY-MM-DD)', '2026-10-10', False),
            'new_home_sample_date': ('string', 'New home sample date (YYYY-MM-DD)', '2026-10-10', False),
            'reason': ('string', 'Reschedule reason', 'Patient request', False),
            'remark': ('string', 'Remark note', 'Updated', False),
            'rescheduled_by': ('string', 'Rescheduled by', 'Staff', False),
        }
    },
    'reschedule_appointment_list': {
        'tag': 'Appointments',
        'method': 'GET',
        'summary': 'List Reschedule Audit Records',
        'description': 'Retrieve list of all appointment reschedule audit logs, optionally filtered by appointment ID.',
        'query_params': {
            'appointment_id': ('integer', 'Filter by appointment ID', False),
        }
    },
    'appointment_cancel_done': {
        'tag': 'Appointments',
        'method': 'POST',
        'summary': 'Cancel Appointment or Upload Report',
        'description': 'Mark appointment as Reports Uploaded or Cancel.',
        'params': {
            'appointment': ('integer', 'Appointment ID', 1, True),
            'status': ('string', 'Reports Uploaded | Cancel', 'Reports Uploaded', True),
            'reason': ('string', 'Cancellation reason', '', False),
            'remark': ('string', 'Remarks', '', False),
            'report_date': ('string', 'Report date (YYYY-MM-DD)', '2026-10-10', False),
        }
    },
    'appointment_date_update': {
        'tag': 'Appointments',
        'method': 'POST',
        'summary': 'Update Appointment Preferred Dates',
        'description': 'Update preferred dates for an appointment.',
        'params': {
            'id': ('integer', 'Appointment ID', 1, True),
            'appointment_date_1': ('string', 'Preferred checkup date 1', '2026-10-01', False),
            'appointment_date_2': ('string', 'Preferred checkup date 2', '2026-10-02', False),
            'home_sample_date_1': ('string', 'Preferred home sample date 1', '2026-10-01', False),
            'home_sample_date_2': ('string', 'Preferred home sample date 2', '2026-10-02', False),
        }
    },
    'all_appointment_list': {
        'tag': 'Appointments',
        'method': 'GET',
        'summary': 'Get All Appointments List',
        'description': 'List all appointments across employees and individuals.',
        'query_params': {
            'page': ('integer', 'Page number', False),
            'page_size': ('integer', 'Page size', False),
            'status': ('string', 'Filter by status', False),
        }
    },
    'employee_appointment_list': {
        'tag': 'Appointments',
        'method': 'POST',
        'summary': 'Get Appointments by Employee',
        'description': 'List all appointments booked for a specific employee.',
        'params': {
            'employee': ('integer', 'Employee ID', 1, True),
        }
    },
    'appointment_list_for_vendor': {
        'tag': 'Appointments',
        'method': 'POST',
        'summary': 'Get Appointments for Vendor',
        'description': 'List all appointments booked with a specific vendor / center.',
        'params': {
            'vendor': ('integer', 'Vendor ID', 1, True),
        }
    },

    # Darwinbox Candidate Appointments
    'darwinbox_candidate_appointment_create': {
        'tag': 'Darwinbox Candidate Appointments',
        'method': 'POST',
        'summary': 'Create Darwinbox Candidate Appointment',
        'description': 'Create an appointment for a Darwinbox pre-employment candidate.',
        'params': {
            'hoh_employee': ('integer', 'HOH Employee / Candidate ID', 101, True),
            'package': ('integer', 'Package ID', 10, True),
            'center': ('integer', 'Center ID', 5, False),
            'vendor': ('integer', 'Vendor ID', 2, False),
            'type_of_visit': ('integer', 'Type of visit ID', 1, False),
            'appointment_date_1': ('string', 'Preferred health checkup date 1', '2026-10-01', False),
            'appointment_date_2': ('string', 'Preferred health checkup date 2', '2026-10-02', False),
            'home_sample_date_1': ('string', 'Preferred home sample date 1', '2026-10-01', False),
            'home_sample_date_2': ('string', 'Preferred home sample date 2', '2026-10-02', False),
            'reason': ('string', 'Reason note', 'Pre-employment', False),
            'remark': ('string', 'Remarks', 'Slot requested', False),
            'status': ('string', 'Status', 'Request Received', False),
        }
    },
    'darwinbox_candidate_appointment_update': {
        'tag': 'Darwinbox Candidate Appointments',
        'method': 'POST',
        'summary': 'Update Darwinbox Candidate Appointment',
        'description': 'Update any fields of a Darwinbox candidate appointment.',
        'params': {
            'id': ('integer', 'Candidate Appointment ID', 1, True),
            'hoh_employee': ('integer', 'HOH Candidate ID', 101, False),
            'package': ('integer', 'Package ID', 10, False),
            'center': ('integer', 'Center ID', 5, False),
            'vendor': ('integer', 'Vendor ID', 2, False),
            'type_of_visit': ('integer', 'Type of visit ID', 1, False),
            'appointment_date_1': ('string', 'Preferred checkup date 1', '2026-10-01', False),
            'appointment_date_2': ('string', 'Preferred checkup date 2', '2026-10-02', False),
            'confirm_appointment_date': ('string', 'Confirmed checkup date', '2026-10-05', False),
            'status': ('string', 'Appointment status', 'Confirmed', False),
            'reason': ('string', 'Reason note', '', False),
            'remark': ('string', 'Remark note', '', False),
        }
    },
    'darwinbox_candidate_appointment_booking_reschedule': {
        'tag': 'Darwinbox Candidate Appointments',
        'method': 'POST',
        'summary': 'Confirm Slot or Reschedule Candidate Appointment',
        'description': 'Confirm candidate appointment or reschedule with audit logging in RescheduleDarwinboxCandidateAppointment.',
        'params': {
            'appointment': ('integer', 'Candidate Appointment ID', 1, True),
            'status': ('string', 'Confirmed | Rescheduled', 'Confirmed', True),
            'confirm_appointment_date': ('string', 'Confirmed checkup date (YYYY-MM-DD)', '2026-10-05', False),
            'confirm_home_sample_date': ('string', 'Confirmed home sample date (YYYY-MM-DD)', '2026-10-05', False),
            'new_appointment_date': ('string', 'New date if rescheduling', '2026-10-10', False),
            'new_home_sample_date': ('string', 'New home sample date if rescheduling', '2026-10-10', False),
            'center': ('integer', 'Center ID', 5, False),
            'rescheduled_by': ('string', 'Rescheduled by', 'Staff', False),
            'reason': ('string', 'Reason', 'Slot requested change', False),
            'remark': ('string', 'Remark', 'Confirmed slot 10 AM', False),
        }
    },
    'darwinbox_candidate_appointment_reschedule': {
        'tag': 'Darwinbox Candidate Appointments',
        'method': 'POST',
        'summary': 'Reschedule Candidate Appointment (Alias)',
        'description': 'Alias endpoint for booking reschedule.',
        'params': {
            'appointment': ('integer', 'Candidate Appointment ID', 1, True),
            'status': ('string', 'Rescheduled', 'Rescheduled', True),
            'new_appointment_date': ('string', 'New checkup date', '2026-10-10', False),
            'reason': ('string', 'Reason', 'Candidate request', False),
            'remark': ('string', 'Remark', '', False),
        }
    },
    'darwinbox_candidate_appointment_cancel_done': {
        'tag': 'Darwinbox Candidate Appointments',
        'method': 'POST',
        'summary': 'Cancel Candidate Appointment or Upload Report',
        'description': 'Mark candidate appointment as Cancel or Reports Uploaded.',
        'params': {
            'appointment': ('integer', 'Candidate Appointment ID', 1, True),
            'status': ('string', 'Reports Uploaded | Cancel', 'Reports Uploaded', True),
            'reason': ('string', 'Reason if cancelled', '', False),
            'remark': ('string', 'Remarks', '', False),
            'report_date': ('string', 'Report date (YYYY-MM-DD)', '2026-10-10', False),
        }
    },
    'darwinbox_candidate_appointment_date_update': {
        'tag': 'Darwinbox Candidate Appointments',
        'method': 'POST',
        'summary': 'Update Candidate Preferred Dates',
        'description': 'Update preferred date selections for candidate appointment.',
        'params': {
            'id': ('integer', 'Appointment ID', 1, True),
            'appointment_date_1': ('string', 'Checkup date 1', '2026-10-01', False),
            'appointment_date_2': ('string', 'Checkup date 2', '2026-10-02', False),
            'home_sample_date_1': ('string', 'Home sample date 1', '2026-10-01', False),
            'home_sample_date_2': ('string', 'Home sample date 2', '2026-10-02', False),
        }
    },
    'all_darwinbox_candidate_appointment_list': {
        'tag': 'Darwinbox Candidate Appointments',
        'method': 'GET',
        'summary': 'List All Candidate Appointments',
        'description': 'Retrieve list of all candidate appointments ordered newest first.',
        'query_params': {
            'page': ('integer', 'Page number', False),
            'page_size': ('integer', 'Page size', False),
        }
    },
    'get_darwinbox_candidate_appointment_detail': {
        'tag': 'Darwinbox Candidate Appointments',
        'method': 'POST',
        'summary': 'Get Candidate Appointment Detail',
        'description': 'Retrieve detailed view of single candidate appointment by ID.',
        'params': {
            'id': ('integer', 'Candidate Appointment ID', 1, True),
        }
    },
    'reschedule_darwinbox_candidate_appointment_list': {
        'tag': 'Darwinbox Candidate Appointments',
        'method': 'GET',
        'summary': 'List Candidate Reschedule Audit Records',
        'description': 'Retrieve audit history of candidate appointment reschedules.',
        'query_params': {
            'appointment_id': ('integer', 'Optional candidate appointment ID filter', False),
        }
    },
    'darwinbox_candidate_appointment_full_manage': {
        'tag': 'Darwinbox Candidate Appointments',
        'method': 'POST',
        'summary': 'Unified Candidate Appointment Manager (All Parameters)',
        'description': 'Unified endpoint accepting ALL parameters for candidate appointment create, update, confirmation, reschedule, and audit logging.',
        'params': {
            'id': ('integer', 'Appointment ID (omit to create new)', 1, False),
            'hoh_employee': ('integer', 'HOH Candidate ID', 101, False),
            'package': ('integer', 'Package ID', 10, False),
            'center': ('integer', 'Center ID', 5, False),
            'vendor': ('integer', 'Vendor ID', 2, False),
            'type_of_visit': ('integer', 'Type of Visit ID', 1, False),
            'appointment_date_1': ('string', 'Preferred checkup date 1', '2026-10-01', False),
            'appointment_date_2': ('string', 'Preferred checkup date 2', '2026-10-02', False),
            'home_sample_date_1': ('string', 'Preferred home sample date 1', '2026-10-01', False),
            'home_sample_date_2': ('string', 'Preferred home sample date 2', '2026-10-02', False),
            'confirm_appointment_date': ('string', 'Confirmed checkup date', '2026-10-05', False),
            'confirm_home_sample_date': ('string', 'Confirmed home sample date', '2026-10-05', False),
            'date_of_appointment': ('string', 'Date of appointment', '2026-10-05', False),
            'new_appointment_date': ('string', 'New date if rescheduling', '2026-10-10', False),
            'new_home_sample_date': ('string', 'New home sample date if rescheduling', '2026-10-10', False),
            'rescheduled_by': ('string', 'Staff/User role', 'Staff', False),
            'reason': ('string', 'Reason note', 'Pre-employment', False),
            'remark': ('string', 'Staff remark', 'Confirmed', False),
            'status': ('string', 'Status: Request Received | Confirmed | Rescheduled | Cancel | Reports Uploaded', 'Confirmed', False),
            'report_date': ('string', 'Report upload date', '2026-10-12', False),
        }
    },

    # Corporates
    'corporate_register': {
        'tag': 'Corporates',
        'method': 'POST',
        'summary': 'Register Corporate',
        'description': 'Create a new corporate client account.',
        'params': {
            'company_name': ('string', 'Corporate company name', 'Acme Corp', True),
            'corporate_code': ('string', 'Unique corporate code', 'ACM001', True),
            'email': ('string', 'Corporate contact email', 'corp@acme.com', True),
            'mobile': ('string', 'Corporate mobile number', '9876543210', True),
            'contact_person': ('string', 'Contact person name', 'John Doe', False),
            'address': ('string', 'Office address', '123 Tech Park', False),
            'city': ('string', 'City', 'Mumbai', False),
            'state': ('string', 'State', 'Maharashtra', False),
            'pincode': ('string', 'Pincode', '400001', False),
            'billing_cycle': ('integer', 'Billing cycle ID', 1, False),
        }
    },
    'corporate_update': {
        'tag': 'Corporates',
        'method': 'POST',
        'summary': 'Update Corporate Details',
        'description': 'Update corporate profile and settings.',
        'params': {
            'id': ('integer', 'Corporate ID', 1, True),
            'company_name': ('string', 'Company name', '', False),
            'email': ('string', 'Email', '', False),
            'mobile': ('string', 'Mobile', '', False),
            'contact_person': ('string', 'Contact person', '', False),
            'status': ('string', 'Active / Inactive', 'Active', False),
        }
    },
    'list_all_corporate': {
        'tag': 'Corporates',
        'method': 'GET',
        'summary': 'List All Corporates',
        'description': 'Retrieve list of all registered corporates.',
        'query_params': {
            'page': ('integer', 'Page number', False),
            'page_size': ('integer', 'Page size', False),
        }
    },

    # Vendors
    'vendor_register': {
        'tag': 'Vendors',
        'method': 'POST',
        'summary': 'Register Vendor',
        'description': 'Create a new diagnostic lab/vendor partner.',
        'params': {
            'vendor_name': ('string', 'Vendor/Lab name', 'Health Labs Inc', True),
            'vendor_code': ('string', 'Unique vendor code', 'HL001', True),
            'email': ('string', 'Vendor email', 'lab@healthlabs.com', True),
            'mobile': ('string', 'Vendor phone', '9876543210', True),
            'address': ('string', 'Lab address', '45 Diagnostic Way', False),
            'city': ('string', 'City', 'Bangalore', False),
            'state': ('string', 'State', 'Karnataka', False),
            'pincode': ('string', 'Pincode', '560001', False),
        }
    },
    'vendor_update': {
        'tag': 'Vendors',
        'method': 'POST',
        'summary': 'Update Vendor Details',
        'description': 'Update vendor details.',
        'params': {
            'id': ('integer', 'Vendor ID', 1, True),
            'vendor_name': ('string', 'Vendor name', '', False),
            'email': ('string', 'Email', '', False),
            'mobile': ('string', 'Mobile', '', False),
            'status': ('string', 'Active / Inactive', 'Active', False),
        }
    },
    'list_all_vendor': {
        'tag': 'Vendors',
        'method': 'GET',
        'summary': 'List All Vendors',
        'description': 'Retrieve list of all vendors.',
        'query_params': {}
    },

    # Employees
    'employee_register': {
        'tag': 'Employees',
        'method': 'POST',
        'summary': 'Register Corporate Employee',
        'description': 'Register an employee under a corporate account.',
        'params': {
            'corporate': ('integer', 'Corporate ID', 1, True),
            'employee_code': ('string', 'Corporate Employee ID/Code', 'EMP001', True),
            'first_name': ('string', 'First name', 'Rahul', True),
            'last_name': ('string', 'Last name', 'Sharma', False),
            'email': ('string', 'Employee email', 'rahul@example.com', True),
            'mobile': ('string', 'Mobile phone', '9876543210', True),
            'gender': ('integer', 'Gender ID', 1, False),
            'dob': ('string', 'Date of birth (YYYY-MM-DD)', '1995-05-15', False),
            'designation': ('string', 'Designation', 'Software Engineer', False),
            'department': ('string', 'Department', 'Engineering', False),
        }
    },
    'employee_update': {
        'tag': 'Employees',
        'method': 'POST',
        'summary': 'Update Employee Details',
        'description': 'Update employee profile.',
        'params': {
            'id': ('integer', 'Employee ID', 1, True),
            'first_name': ('string', 'First name', '', False),
            'last_name': ('string', 'Last name', '', False),
            'email': ('string', 'Email', '', False),
            'mobile': ('string', 'Mobile', '', False),
            'status': ('string', 'Active / Inactive', 'Active', False),
        }
    },
    'list_all_employee': {
        'tag': 'Employees',
        'method': 'GET',
        'summary': 'List All Employees',
        'description': 'Retrieve list of all employees.',
        'query_params': {
            'corporate_id': ('integer', 'Filter by Corporate ID', False),
            'page': ('integer', 'Page number', False),
        }
    },

    # Packages
    'package_create': {
        'tag': 'Packages',
        'method': 'POST',
        'summary': 'Create Health Package',
        'description': 'Create a new health checkup package.',
        'params': {
            'package_name': ('string', 'Package name', 'Executive Full Body Health Package', True),
            'vendor': ('integer', 'Vendor ID', 1, True),
            'type_of_visit': ('integer', 'Type of Visit ID (Home/Center)', 1, True),
            'price': ('number', 'Package price', 1999.00, True),
            'description': ('string', 'Package description and inclusions', 'Complete 70+ test checkup', False),
            'age_category': ('integer', 'Age Category ID', 1, False),
            'gender': ('integer', 'Gender ID (Male/Female/All)', 1, False),
        }
    },
    'package_update': {
        'tag': 'Packages',
        'method': 'POST',
        'summary': 'Update Health Package',
        'description': 'Update health package details.',
        'params': {
            'id': ('integer', 'Package ID', 1, True),
            'package_name': ('string', 'Package name', '', False),
            'price': ('number', 'Price', 1999.00, False),
            'status': ('string', 'Active / Inactive', 'Active', False),
        }
    },
    'list_all_package': {
        'tag': 'Packages',
        'method': 'GET',
        'summary': 'List All Packages',
        'description': 'Retrieve list of all packages.',
        'query_params': {}
    },

    # Centers
    'center_create': {
        'tag': 'Centers',
        'method': 'POST',
        'summary': 'Create Diagnostic Center',
        'description': 'Create diagnostic center/branch for vendor.',
        'params': {
            'vendor': ('integer', 'Vendor ID', 1, True),
            'center_name': ('string', 'Center name', 'City Center Lab Branch', True),
            'address': ('string', 'Center address', '12 Main Road', True),
            'city': ('string', 'City', 'Mumbai', True),
            'state': ('string', 'State', 'Maharashtra', True),
            'pincode': ('string', 'Pincode', '400001', True),
            'latitude': ('string', 'Latitude coordinates', '19.0760', False),
            'longitude': ('string', 'Longitude coordinates', '72.8777', False),
        }
    },
    'list_all_center': {
        'tag': 'Centers',
        'method': 'GET',
        'summary': 'List All Diagnostic Centers',
        'description': 'Retrieve list of all diagnostic centers.',
        'query_params': {
            'vendor_id': ('integer', 'Filter by Vendor ID', False),
        }
    },

    # Cart & Transactions
    'add_to_cart_create': {
        'tag': 'Cart & Orders',
        'method': 'POST',
        'summary': 'Add Package to Cart',
        'description': 'Add health package to cart for checkout.',
        'params': {
            'package': ('integer', 'Package ID', 1, True),
            'individual': ('integer', 'Individual User ID', 1, False),
            'employee': ('integer', 'Employee ID', 1, False),
            'quantity': ('integer', 'Quantity', 1, False),
        }
    },
    'add_to_cart_list': {
        'tag': 'Cart & Orders',
        'method': 'GET',
        'summary': 'Get Cart Items',
        'description': 'Retrieve all items in cart for user.',
        'query_params': {
            'individual_id': ('integer', 'Individual user ID', False),
            'employee_id': ('integer', 'Employee ID', False),
        }
    },
    'add_to_cart_delete': {
        'tag': 'Cart & Orders',
        'method': 'POST',
        'summary': 'Remove Item from Cart',
        'description': 'Remove package item from cart.',
        'params': {
            'id': ('integer', 'Cart Item ID', 1, True),
        }
    },
}


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    """
    Enhanced OpenAPI Schema Generator that automatically discovers and generates
    rich documentation for all Svasthya endpoints.
    """

    def get_schema(self, request=None, public=False):
        schema = super(CustomOpenAPISchemaGenerator, self).get_schema(request, public)
        
        # Discover all URL patterns from svasthyapp.urls
        resolver = get_resolver()
        self._populate_all_endpoints(schema, resolver)
        
        return schema

    def _populate_all_endpoints(self, schema, resolver):
        try:
            import svasthyapp.urls as app_urls
            urlpatterns = app_urls.urlpatterns
        except Exception:
            urlpatterns = []

        type_map = {
            'string': openapi.TYPE_STRING,
            'integer': openapi.TYPE_INTEGER,
            'number': openapi.TYPE_NUMBER,
            'boolean': openapi.TYPE_BOOLEAN,
        }

        for pattern in urlpatterns:
            try:
                path_str = getattr(pattern.pattern, '_route', None)
                if not path_str:
                    regex_pat = getattr(pattern.pattern, 'regex', None)
                    if regex_pat:
                        raw = regex_pat.pattern.lstrip('^').rstrip('\\Z$').rstrip('$')
                        path_str = '/' + raw.lstrip('/')
                    else:
                        continue

                if not path_str.startswith('/'):
                    path_str = '/' + path_str
                if not path_str.endswith('/'):
                    path_str = path_str + '/'

                # Skip internal or swagger routes
                if any(x in path_str for x in ['swagger', 'redoc', 'media', 'static', 'admin']):
                    continue

                view_func = pattern.callback
                func_name = getattr(view_func, '__name__', '')
                view_name = getattr(pattern, 'name', func_name)

                # Check if already present in paths
                existing_path = schema.paths.get(path_str, None)
                if existing_path and len(existing_path) > 0:
                    continue

                # Determine metadata
                meta = ENDPOINT_METADATA.get(func_name) or ENDPOINT_METADATA.get(view_name)
                
                # Derive tag from route or name
                if meta and 'tag' in meta:
                    tag = meta['tag']
                else:
                    tag = self._derive_tag(path_str, func_name)

                method = (meta.get('method') if meta else self._infer_method(func_name, path_str)).lower()
                summary = meta.get('summary') if meta else self._make_title(func_name)
                description = meta.get('description') if meta else f"Endpoint: {func_name}. Provides API service for {tag}."

                parameters = []
                request_body = None

                if meta and 'query_params' in meta:
                    for qname, qinfo in meta['query_params'].items():
                        qtype, qdesc, qreq = qinfo
                        parameters.append(openapi.Parameter(
                            name=qname,
                            in_=openapi.IN_QUERY,
                            description=qdesc,
                            type=type_map.get(qtype, openapi.TYPE_STRING),
                            required=qreq
                        ))

                if meta and 'params' in meta:
                    if method in ['post', 'put', 'patch', 'delete']:
                        props = {}
                        req_fields = []
                        for pname, pinfo in meta['params'].items():
                            ptype, pdesc, pex, preq = pinfo
                            props[pname] = openapi.Schema(
                                type=type_map.get(ptype, openapi.TYPE_STRING),
                                description=pdesc,
                                example=pex
                            )
                            if preq:
                                req_fields.append(pname)
                        request_body = openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties=props,
                            required=req_fields if req_fields else None
                        )
                    else:
                        for pname, pinfo in meta['params'].items():
                            ptype, pdesc, pex, preq = pinfo
                            parameters.append(openapi.Parameter(
                                name=pname,
                                in_=openapi.IN_QUERY,
                                description=pdesc,
                                type=type_map.get(ptype, openapi.TYPE_STRING),
                                required=preq
                            ))
                elif method in ['post', 'put', 'patch']:
                    # Generate default body schema for POST requests
                    props = self._infer_params_from_name(func_name)
                    request_body = openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties=props,
                        description=f"Payload for {func_name}"
                    )

                responses = openapi.Responses({
                    200: openapi.Response(
                        description="Success",
                        schema=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'statuscode': openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                                'status': openapi.Schema(type=openapi.TYPE_STRING, example='true'),
                                'message': openapi.Schema(type=openapi.TYPE_STRING, example='Operation successful'),
                                'data': openapi.Schema(type=openapi.TYPE_OBJECT, description='Response data payload')
                            }
                        )
                    )
                })

                operation = openapi.Operation(
                    operation_id=f"{func_name}_{method}",
                    summary=summary,
                    description=description,
                    tags=[tag],
                    parameters=parameters if parameters else None,
                    request_body=request_body,
                    responses=responses
                )

                if path_str not in schema.paths:
                    schema.paths[path_str] = openapi.PathItem()

                setattr(schema.paths[path_str], method, operation)

            except Exception:
                continue

    def _derive_tag(self, path_str, func_name):
        path_lower = path_str.lower()
        if 'darwinbox' in path_lower:
            return 'Darwinbox Candidate Appointments'
        elif any(x in path_lower for x in ['appointment', 'booking', 'reschedule']):
            return 'Appointments'
        elif 'corporate' in path_lower:
            return 'Corporates'
        elif 'vendor' in path_lower:
            return 'Vendors'
        elif 'employee' in path_lower:
            return 'Employees'
        elif 'individual' in path_lower:
            return 'Individuals'
        elif 'package' in path_lower:
            return 'Packages'
        elif 'center' in path_lower:
            return 'Centers'
        elif 'cart' in path_lower:
            return 'Cart & Orders'
        elif 'transaction' in path_lower or 'payment' in path_lower:
            return 'Payments & Transactions'
        elif 'health_tips' in path_lower:
            return 'Health Tips'
        elif 'holiday' in path_lower:
            return 'Holidays'
        elif 'test' in path_lower:
            return 'Test Categories & Tests'
        elif any(x in path_lower for x in ['staff_department', 'type_of_access', 'staff_level', 'staff_type', 'age_category', 'gender', 'relation', 'type_of_service', 'type_of_visit', 'parent_company', 'billing_cycle', 'weekdays', 'payment_tags', 'type_of_industry', 'duration', 'platform']):
            return 'Masters Tables'
        elif 'staff' in path_lower:
            return 'Staff'
        elif 'notification' in path_lower:
            return 'Notifications'
        elif 'export' in path_lower:
            return 'Data Export'
        elif 'import' in path_lower:
            return 'Bulk Import'
        else:
            return 'General Services'

    def _infer_method(self, func_name, path_str):
        name = (func_name + ' ' + path_str).lower()
        if any(x in name for x in ['list', 'detail', 'get', 'check', 'view']):
            return 'GET'
        return 'POST'

    def _make_title(self, name):
        return ' '.join(word.capitalize() for word in name.replace('_', ' ').split())

    def _infer_params_from_name(self, func_name):
        name = func_name.lower()
        props = {}
        if 'delete' in name or 'detail' in name or 'update' in name:
            props['id'] = openapi.Schema(type=openapi.TYPE_INTEGER, description='Target object ID', example=1)
        if 'create' in name or 'update' in name or 'register' in name:
            props['name'] = openapi.Schema(type=openapi.TYPE_STRING, description='Name / Title', example='Sample')
            props['status'] = openapi.Schema(type=openapi.TYPE_STRING, description='Status', example='Active')
        if 'status' in name:
            props['id'] = openapi.Schema(type=openapi.TYPE_INTEGER, description='ID', example=1)
            props['status'] = openapi.Schema(type=openapi.TYPE_STRING, description='Active / Inactive', example='Active')
        if not props:
            props['data'] = openapi.Schema(type=openapi.TYPE_OBJECT, description='Payload object')
        return props


# Reusable Schema View configured with CustomOpenAPISchemaGenerator
schema_view = get_schema_view(
    openapi.Info(
        title="Svasthya Complete API Documentation",
        default_version='v1',
        description="""
# Svasthya Interactive REST API Documentation

Comprehensive API explorer with full parameter schemas and request bodies for:
- **Darwinbox Candidate Appointments & Rescheduling**
- **Employee & Individual Health Appointments**
- **Masters Tables (Department, Level, Access, Service, Visit, Gender, etc.)**
- **Corporates, Vendors, Employees & Diagnostic Centers**
- **Health Packages, Cart, Orders & Payments**
        """,
        contact=openapi.Contact(email="support@svasthya.com"),
        license=openapi.License(name="Private"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=CustomOpenAPISchemaGenerator,
)


def api_endpoints_catalog(request):
    """
    JSON Directory of all endpoints and parameter specifications.
    Access at /api/swagger-endpoints/
    """
    generator = CustomOpenAPISchemaGenerator(
        openapi.Info(
            title="Svasthya Endpoints Directory",
            default_version='v1'
        )
    )
    schema = generator.get_schema(request=None, public=True)
    
    catalog = {}
    for path, path_item in schema.paths.items():
        methods_dict = {}
        for method, op in getattr(path_item, 'operations', []):
            if op:
                params = []
                if hasattr(op, 'parameters') and op.parameters:
                    for p in op.parameters:
                        params.append({
                            'name': getattr(p, 'name', ''),
                            'in': getattr(p, 'in_', 'query'),
                            'type': getattr(p, 'type', 'string'),
                            'required': getattr(p, 'required', False),
                            'description': getattr(p, 'description', '')
                        })
                body = None
                if hasattr(op, 'request_body') and op.request_body and hasattr(op.request_body, 'properties') and op.request_body.properties:
                    body = {k: getattr(v, 'description', '') for k, v in op.request_body.properties.items()}
                
                methods_dict[method.upper()] = {
                    'summary': getattr(op, 'summary', ''),
                    'tags': getattr(op, 'tags', []),
                    'parameters': params,
                    'request_body': body,
                    'description': getattr(op, 'description', '')
                }
        if methods_dict:
            catalog[path] = methods_dict

    return JsonResponse({
        'statuscode': 200,
        'status': 'true',
        'total_endpoints': len(catalog),
        'swagger_ui_url': '/api/swagger/',
        'endpoints': catalog
    }, json_dumps_params={'indent': 2})
