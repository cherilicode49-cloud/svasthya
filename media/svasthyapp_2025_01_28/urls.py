from django.urls import path
from svasthyapp import views

from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('api/admin_login/', views.admin_login, name = 'admin_login'),
    
    path('api/send_otp/', views.send_otp, name = 'send_otp'),
    path('api/verify_otp/', views.verify_otp, name = 'verify_otp'),
    
    #### MASTERS TABLES ####
    ## Staff Department
    path('api/staff_department_create/', views.staff_department_create, name = 'staff_department_create'),
    path('api/staff_department_update/', views.staff_department_update, name = 'staff_department_update'),
    path('api/all_staff_department_list/', views.all_staff_department_list, name = 'all_staff_department_list'),
    path('api/all_active_staff_department_list/', views.all_active_staff_department_list, name = 'all_active_staff_department_list'),

    ## Type OF access
    path('api/type_of_access_create/', views.type_of_access_create, name = 'type_of_access_create'),
    path('api/type_of_access_update/', views.type_of_access_update, name = 'type_of_access_update'),
    path('api/all_type_of_access_list/', views.all_type_of_access_list, name = 'all_type_of_access_list'),
    path('api/all_active_type_of_access_list/', views.all_active_type_of_access_list, name = 'all_active_type_of_access_list'),

    ## Staff Level
    path('api/staff_level_create/', views.staff_level_create, name = 'staff_level_create'),
    path('api/staff_level_update/', views.staff_level_update, name = 'staff_level_update'),
    path('api/all_staff_level_list/', views.all_staff_level_list, name = 'all_staff_level_list'),
    path('api/all_active_staff_level_list/', views.all_active_staff_level_list, name = 'all_active_staff_level_list'),

    ## Staff Type
    path('api/staff_type_create/', views.staff_type_create, name = 'staff_type_create'),
    path('api/staff_type_update/', views.staff_type_update, name = 'staff_type_update'),
    path('api/all_staff_type_list/', views.all_staff_type_list, name = 'all_staff_type_list'),
    path('api/all_active_staff_type_list/', views.all_active_staff_type_list, name = 'all_active_staff_type_list'),

    ## Age Category
    path('api/age_category_create/', views.age_category_create, name = 'age_category_create'),
    path('api/age_category_update/', views.age_category_update, name = 'age_category_update'),
    path('api/all_age_category_list/', views.all_age_category_list, name = 'all_age_category_list'),
    path('api/all_active_age_category_list/', views.all_active_age_category_list, name = 'all_active_age_category_list'),

    ## Gender
    path('api/gender_create/', views.gender_create, name = 'gender_create'),
    path('api/gender_update/', views.gender_update, name = 'gender_update'),
    path('api/all_gender_list/', views.all_gender_list, name = 'all_gender_list'),
    path('api/all_active_gender_list/', views.all_active_gender_list, name = 'all_active_gender_list'),

    ## Relation
    path('api/relation_create/', views.relation_create, name = 'relation_create'),
    path('api/relation_update/', views.relation_update, name = 'relation_update'),
    path('api/all_relation_list/', views.all_relation_list, name = 'all_relation_list'),
    path('api/all_active_relation_list/', views.all_active_relation_list, name = 'all_active_relation_list'),

    ## Type of Service 
    path('api/type_of_service_create/', views.type_of_service_create, name = 'type_of_service_create'),
    path('api/type_of_service_update/', views.type_of_service_update, name = 'type_of_service_update'),
    path('api/all_type_of_service_list/', views.all_type_of_service_list, name = 'all_type_of_service_list'),
    path('api/all_active_type_of_service_list/', views.all_active_type_of_service_list, name = 'all_active_type_of_service_list'),

    ## Type of Visit 
    path('api/type_of_visit_create/', views.type_of_visit_create, name = 'type_of_visit_create'),
    path('api/type_of_visit_update/', views.type_of_visit_update, name = 'type_of_visit_update'),
    path('api/all_type_of_visit_list/', views.all_type_of_visit_list, name = 'all_type_of_visit_list'),
    path('api/all_active_type_of_visit_list/', views.all_active_type_of_visit_list, name = 'all_active_type_of_visit_list'),

    ## Parent Company
    path('api/parent_company_create/', views.parent_company_create, name = 'parent_company_create'),
    path('api/parent_company_update/', views.parent_company_update, name = 'parent_company_update'),
    path('api/all_parent_company_list/', views.all_parent_company_list, name = 'all_parent_company_list'),
    path('api/all_active_parent_company_list/', views.all_active_parent_company_list, name = 'all_active_parent_company_list'),


    ## Billing Cycle 
    path('api/billing_cycle_create/', views.billing_cycle_create, name = 'billing_cycle_create'),
    path('api/billing_cycle_update/', views.billing_cycle_update, name = 'billing_cycle_update'),
    path('api/all_billing_cycle_list/', views.all_billing_cycle_list, name = 'all_billing_cycle_list'),
    path('api/all_active_billing_cycle_list/', views.all_active_billing_cycle_list, name = 'all_active_billing_cycle_list'),

    ## Weekdays
    path('api/weekdays_create/', views.weekdays_create, name = 'weekdays_create'),
    path('api/weekdays_update/', views.weekdays_update, name = 'weekdays_update'),
    path('api/all_weekdays_list/', views.all_weekdays_list, name = 'all_weekdays_list'),
    path('api/all_active_weekdays_list/', views.all_active_weekdays_list, name = 'all_active_weekdays_list'),


    ## Holidays
    path('api/holidays_create/', views.holidays_create, name = 'holidays_create'),
    path('api/holidays_update/', views.holidays_update, name = 'holidays_update'),
    path('api/all_holidays_list/', views.all_holidays_list, name = 'all_holidays_list'),
    path('api/all_active_holidays_list/', views.all_active_holidays_list, name = 'all_active_holidays_list'),

    ## Payment Tags
    path('api/payment_tags_create/', views.payment_tags_create, name = 'payment_tags_create'),
    path('api/payment_tags_update/', views.payment_tags_update, name = 'payment_tags_update'),
    path('api/all_payment_tags_list/', views.all_payment_tags_list, name = 'all_payment_tags_list'),
    path('api/all_active_payment_tags_list/', views.all_active_payment_tags_list, name = 'all_active_payment_tags_list'),
    
    


    ## Staff
    path('api/staff_register/', views.staff_register, name = 'staff_register'),
    path('api/list_all_staff/', views.list_all_staff, name = 'list_all_staff'),
    path('api/staff_status_update/', views.staff_status_update, name = 'staff_status_update'),
    path('api/staff_update/', views.staff_update, name = 'staff_update'),
    path('api/active_all_staff/', views.active_all_staff, name = 'active_all_staff'),
    path('api/list_only_staff/', views.list_only_staff, name = 'list_only_staff'),
    path('api/staff_profile_image_update/', views.staff_profile_image_update, name = 'staff_profile_image_update'),
    path('api/admin_staff_data_update_request/', views.admin_staff_data_update_request, name = 'admin_staff_data_update_request'),
    
    


   
    ### Corporate
    path('api/corporate_register/', views.corporate_register, name = 'corporate_register'),
    path('api/list_all_corporate/', views.list_all_corporate, name = 'list_all_corporate'),
    path('api/corporate_update/', views.corporate_update, name = 'corporate_update'),
    path('api/corporate_status_update/', views.corporate_status_update, name = 'corporate_status_update'),
    path('api/active_all_corporate/', views.active_all_corporate, name = 'active_all_corporate'),
    path('api/corporate_code_check/', views.corporate_code_check, name = 'corporate_code_check'),
    path('api/corporate_package_list/', views.corporate_package_list, name = 'corporate_package_list'),
    path('api/corporate_delete_inactive/', views.corporate_delete_inactive, name = 'corporate_delete_inactive'),
    

    ### vendor
    path('api/vendor_register/', views.vendor_register, name = 'vendor_register'),
    path('api/list_all_vendor/', views.list_all_vendor, name = 'list_all_vendor'),
    path('api/vendor_update/', views.vendor_update, name = 'vendor_update'),
    path('api/vendor_status_update/', views.vendor_status_update, name = 'vendor_status_update'),
    path('api/all_active_vendor/', views.all_active_vendor, name = 'all_active_vendor'),
    path('api/vendor_code_check/', views.vendor_code_check, name = 'vendor_code_check'),
    path('api/vendor_delete_inactive/', views.vendor_delete_inactive, name = 'vendor_delete_inactive'),
    path('api/vendor_profile_image_update/', views.vendor_profile_image_update, name = 'vendor_profile_image_update'),
    
    
    
    ### Employee
    path('api/employee_register/', views.employee_register, name = 'employee_register'),
    path('api/employee_update/', views.employee_update, name = 'employee_update'),
    path('api/employee_status_update/', views.employee_status_update, name = 'employee_status_update'),
    path('api/list_all_employee/', views.list_all_employee, name = 'list_all_employee'),
    path('api/active_employee_list/', views.active_employee_list, name = 'active_employee_list'),
    path('api/employee_list_by_corporate/', views.employee_list_by_corporate, name = 'employee_list_by_corporate'),
    path('api/employee_dependent_list/', views.employee_dependent_list, name = 'employee_dependent_list'),
    path('api/employee_data_update/', views.employee_data_update, name = 'employee_data_update'),
    path('api/new_employee_dependent_request/', views.new_employee_dependent_request, name = 'new_employee_dependent_request'),
    path('api/employee_profile_image_update/', views.employee_profile_image_update, name = 'employee_profile_image_update'),
    path('api/employee_delete_inactive/', views.employee_delete_inactive, name = 'employee_delete_inactive'),
    

    # ### Package
    path('api/package_create/', views.package_create, name = 'package_create'),
    path('api/package_update/', views.package_update, name = 'package_update'),
    path('api/package_status_update/', views.package_status_update, name = 'package_status_update'),
    path('api/list_all_package/', views.list_all_package, name = 'list_all_package'),
    path('api/all_active_package/', views.all_active_package, name = 'all_active_package'),
    path('api/service_wise_package_list_employee/', views.service_wise_package_list_employee, name = 'service_wise_package_list_employee'),
    path('api/package_list_employee/', views.package_list_employee, name = 'package_list_employee'),
    path('api/search_package/', views.search_package, name = 'search_package'),
    path('api/package_delete_inactive/', views.package_delete_inactive, name = 'package_delete_inactive'),
    
    
    ### Center
    path('api/center_create/', views.center_create, name = 'center_create'),
    path('api/center_update/', views.center_update, name = 'center_update'),
    path('api/center_status_update/', views.center_status_update, name = 'center_status_update'),
    path('api/list_all_center/', views.list_all_center, name = 'list_all_center'),
    path('api/center_serivce_list_by_vendor/', views.center_serivce_list_by_vendor, name = 'center_serivce_list_by_vendor'),
    path('api/center_delete_inactive/', views.center_delete_inactive, name = 'center_delete_inactive'),
    
    

    ### Holiday
    path('api/holiday_create/', views.holiday_create, name = 'holiday_create'),
    path('api/holiday_update/', views.holiday_update, name = 'holiday_update'),
    path('api/holiday_status_update/', views.holiday_status_update, name = 'holiday_status_update'),
    path('api/list_all_holiday/', views.list_all_holiday, name = 'list_all_holiday'),
    path('api/holiday_delete_inactive/', views.holiday_delete_inactive, name = 'holiday_delete_inactive'),
    
    
    ### Health Tips
    path('api/health_tips_create/', views.health_tips_create, name = 'health_tips_create'),
    path('api/health_tips_update/', views.health_tips_update, name = 'health_tips_update'),
    path('api/health_tips_status_update/', views.health_tips_status_update, name = 'health_tips_status_update'),
    path('api/list_all_health_tips/', views.list_all_health_tips, name = 'list_all_health_tips'),
    path('api/list_active_health_tips/', views.list_active_health_tips, name = 'list_active_health_tips'),
    path('api/active_inactive_health_tips/', views.active_inactive_health_tips, name = 'active_inactive_health_tips'),
    
    #### Appionment
    path('api/appoinment_create/', views.appoinment_create, name = 'appoinment_create'),
    path('api/all_appoinment_list/', views.all_appoinment_list, name = 'all_appoinment_list'),
    path('api/employee_appoinment_list/', views.employee_appoinment_list, name = 'employee_appoinment_list'),
    path('api/appoinment_booking_reschedule/', views.appoinment_booking_reschedule, name = 'appoinment_booking_reschedule'),
    path('api/appoinment_list_for_vendor/', views.appoinment_list_for_vendor, name = 'appoinment_list_for_vendor'),
    path('api/appoinment_cancel_done/', views.appoinment_cancel_done, name = 'appoinment_cancel_done'),
    path('api/appoinment_delete_inactive/', views.appoinment_delete_inactive, name = 'appoinment_delete_inactive'),
    path('api/appoinment_data_check/', views.appoinment_data_check, name = 'appoinment_data_check'),
    
    
    #### Bulk Import
    path('api/bulk_import/', views.bulk_import, name = 'bulk_import'),
    path('api/bulk_import_submit/', views.bulk_import_submit, name = 'bulk_import_submit'),

    ### redirect
    path('api/redirect_login_wellness/', views.redirect_login_wellness, name = 'redirect_login_wellness'),    
    path('api/encrypt_data/', views.encrypt_data, name = 'encrypt_data'),
    

     

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
