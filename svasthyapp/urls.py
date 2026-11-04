from django.urls import path
from svasthyapp import swagger, views
from svasthyapp.apis import (
    auth_apis,
    masters_apis,
    staff_apis,
    corporate_apis,
    vendor_apis,
    employee_apis,
    individual_apis,
    package_apis,
    center_apis,
    appointment_apis,
    orders_billing_apis,
    engagement_apis,
    darwinbox_sync,
    hoh_employee,
    candidate_appointments,
)

from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('api/admin_login/', auth_apis.admin_login, name = 'admin_login'),
    
    path('api/send_otp/', auth_apis.send_otp, name = 'send_otp'),
    path('api/verify_otp/', auth_apis.verify_otp, name = 'verify_otp'),
    
    #### MASTERS TABLES ####
    ## Staff Department
    path('api/staff_department_create/', masters_apis.staff_department_create, name = 'staff_department_create'),
    path('api/staff_department_update/', masters_apis.staff_department_update, name = 'staff_department_update'),
    path('api/all_staff_department_list/', masters_apis.all_staff_department_list, name = 'all_staff_department_list'),
    path('api/all_active_staff_department_list/', masters_apis.all_active_staff_department_list, name = 'all_active_staff_department_list'),
    path('api/staff_department_delete_inactive/', masters_apis.staff_department_delete_inactive, name = 'staff_department_delete_inactive'),

    ## Type OF access
    path('api/type_of_access_create/', masters_apis.type_of_access_create, name = 'type_of_access_create'),
    path('api/type_of_access_update/', masters_apis.type_of_access_update, name = 'type_of_access_update'),
    path('api/all_type_of_access_list/', masters_apis.all_type_of_access_list, name = 'all_type_of_access_list'),
    path('api/all_active_type_of_access_list/', masters_apis.all_active_type_of_access_list, name = 'all_active_type_of_access_list'),
    path('api/type_of_access_delete_inactive/', masters_apis.type_of_access_delete_inactive, name = 'type_of_access_delete_inactive'),

    ## Staff Level
    path('api/staff_level_create/', masters_apis.staff_level_create, name = 'staff_level_create'),
    path('api/staff_level_update/', masters_apis.staff_level_update, name = 'staff_level_update'),
    path('api/all_staff_level_list/', masters_apis.all_staff_level_list, name = 'all_staff_level_list'),
    path('api/all_active_staff_level_list/', masters_apis.all_active_staff_level_list, name = 'all_active_staff_level_list'),
    path('api/staff_level_delete_inactive/', masters_apis.staff_level_delete_inactive, name = 'staff_level_delete_inactive'),

    ## Staff Type
    path('api/staff_type_create/', masters_apis.staff_type_create, name = 'staff_type_create'),
    path('api/staff_type_update/', masters_apis.staff_type_update, name = 'staff_type_update'),
    path('api/all_staff_type_list/', masters_apis.all_staff_type_list, name = 'all_staff_type_list'),
    path('api/all_active_staff_type_list/', masters_apis.all_active_staff_type_list, name = 'all_active_staff_type_list'),
    path('api/staff_type_delete_inactive/', masters_apis.staff_type_delete_inactive, name = 'staff_type_delete_inactive'),

    ## Age Category
    path('api/age_category_create/', masters_apis.age_category_create, name = 'age_category_create'),
    path('api/age_category_update/', masters_apis.age_category_update, name = 'age_category_update'),
    path('api/all_age_category_list/', masters_apis.all_age_category_list, name = 'all_age_category_list'),
    path('api/all_active_age_category_list/', masters_apis.all_active_age_category_list, name = 'all_active_age_category_list'),
    path('api/age_category_delete_inactive/', masters_apis.age_category_delete_inactive, name = 'age_category_delete_inactive'),

    ## Gender
    path('api/gender_create/', masters_apis.gender_create, name = 'gender_create'),
    path('api/gender_update/', masters_apis.gender_update, name = 'gender_update'),
    path('api/all_gender_list/', masters_apis.all_gender_list, name = 'all_gender_list'),
    path('api/all_active_gender_list/', masters_apis.all_active_gender_list, name = 'all_active_gender_list'),
    path('api/gender_delete_inactive/', masters_apis.gender_delete_inactive, name = 'gender_delete_inactive'),

    ## Relation
    path('api/relation_create/', masters_apis.relation_create, name = 'relation_create'),
    path('api/relation_update/', masters_apis.relation_update, name = 'relation_update'),
    path('api/all_relation_list/', masters_apis.all_relation_list, name = 'all_relation_list'),
    path('api/all_active_relation_list/', masters_apis.all_active_relation_list, name = 'all_active_relation_list'),
    path('api/relation_delete_inactive/', masters_apis.relation_delete_inactive, name = 'relation_delete_inactive'),

    ## Type of Service 
    path('api/type_of_service_create/', masters_apis.type_of_service_create, name = 'type_of_service_create'),
    path('api/type_of_service_update/', masters_apis.type_of_service_update, name = 'type_of_service_update'),
    path('api/all_type_of_service_list/', masters_apis.all_type_of_service_list, name = 'all_type_of_service_list'),
    path('api/all_active_type_of_service_list/', masters_apis.all_active_type_of_service_list, name = 'all_active_type_of_service_list'),
    path('api/type_of_service_delete_inactive/', masters_apis.type_of_service_delete_inactive, name = 'type_of_service_delete_inactive'),

    ## Type of Visit 
    path('api/type_of_visit_create/', masters_apis.type_of_visit_create, name = 'type_of_visit_create'),
    path('api/type_of_visit_update/', masters_apis.type_of_visit_update, name = 'type_of_visit_update'),
    path('api/all_type_of_visit_list/', masters_apis.all_type_of_visit_list, name = 'all_type_of_visit_list'),
    path('api/all_active_type_of_visit_list/', masters_apis.all_active_type_of_visit_list, name = 'all_active_type_of_visit_list'),
    path('api/type_of_visit_delete_inactive/', masters_apis.type_of_visit_delete_inactive, name = 'type_of_visit_delete_inactive'),

    ## Parent Company
    path('api/parent_company_create/', masters_apis.parent_company_create, name = 'parent_company_create'),
    path('api/parent_company_update/', masters_apis.parent_company_update, name = 'parent_company_update'),
    path('api/all_parent_company_list/', masters_apis.all_parent_company_list, name = 'all_parent_company_list'),
    path('api/all_active_parent_company_list/', masters_apis.all_active_parent_company_list, name = 'all_active_parent_company_list'),
    path('api/parent_company_delete_inactive/', masters_apis.parent_company_delete_inactive, name = 'parent_company_delete_inactive'),


    ## Billing Cycle 
    path('api/billing_cycle_create/', masters_apis.billing_cycle_create, name = 'billing_cycle_create'),
    path('api/billing_cycle_update/', masters_apis.billing_cycle_update, name = 'billing_cycle_update'),
    path('api/all_billing_cycle_list/', masters_apis.all_billing_cycle_list, name = 'all_billing_cycle_list'),
    path('api/all_active_billing_cycle_list/', masters_apis.all_active_billing_cycle_list, name = 'all_active_billing_cycle_list'),
    path('api/billing_cycle_delete_inactive/', masters_apis.billing_cycle_delete_inactive, name = 'billing_cycle_delete_inactive'),

    ## Weekdays
    path('api/weekdays_create/', masters_apis.weekdays_create, name = 'weekdays_create'),
    path('api/weekdays_update/', masters_apis.weekdays_update, name = 'weekdays_update'),
    path('api/all_weekdays_list/', masters_apis.all_weekdays_list, name = 'all_weekdays_list'),
    path('api/all_active_weekdays_list/', masters_apis.all_active_weekdays_list, name = 'all_active_weekdays_list'),
    path('api/weekdays_delete_inactive/', masters_apis.weekdays_delete_inactive, name = 'weekdays_delete_inactive'),

    ## Holidays
    path('api/holidays_create/', masters_apis.holidays_create, name = 'holidays_create'),
    path('api/holidays_update/', masters_apis.holidays_update, name = 'holidays_update'),
    path('api/all_holidays_list/', center_apis.all_holidays_list, name = 'all_holidays_list'),
    path('api/all_active_holidays_list/', masters_apis.all_active_holidays_list, name = 'all_active_holidays_list'),
    path('api/holidays_delete_inactive/', masters_apis.holidays_delete_inactive, name = 'holidays_delete_inactive'),

    ## Payment Tags
    path('api/payment_tags_create/', masters_apis.payment_tags_create, name = 'payment_tags_create'),
    path('api/payment_tags_update/', masters_apis.payment_tags_update, name = 'payment_tags_update'),
    path('api/all_payment_tags_list/', orders_billing_apis.all_payment_tags_list, name = 'all_payment_tags_list'),
    path('api/all_active_payment_tags_list/', masters_apis.all_active_payment_tags_list, name = 'all_active_payment_tags_list'),
    path('api/payment_tags_delete_inactive/', masters_apis.payment_tags_delete_inactive, name = 'payment_tags_delete_inactive'),
    
    ## Type of industry
    path('api/type_of_industry_create/', masters_apis.type_of_industry_create, name = 'type_of_industry_create'),
    path('api/type_of_industry_update/', masters_apis.type_of_industry_update, name = 'type_of_industry_update'),
    path('api/all_type_of_industry_list/', masters_apis.all_type_of_industry_list, name = 'all_type_of_industry_list'),
    path('api/all_active_type_of_industry_list/', masters_apis.all_active_type_of_industry_list, name = 'all_active_type_of_industry_list'),
    path('api/type_of_industry_delete_inactive/', masters_apis.type_of_industry_delete_inactive, name = 'type_of_industry_delete_inactive'),

    ## Duration
    path('api/duration_create/', masters_apis.duration_create, name = 'duration_create'),
    path('api/duration_update/', masters_apis.duration_update, name = 'duration_update'),
    path('api/all_duration_list/', masters_apis.all_duration_list, name = 'all_duration_list'),
    path('api/all_active_duration_list/', masters_apis.all_active_duration_list, name = 'all_active_duration_list'),
    path('api/duration_delete_inactive/', masters_apis.duration_delete_inactive, name = 'duration_delete_inactive'),

    ## Platform
    path('api/platform_create/', masters_apis.platform_create, name = 'platform_create'),
    path('api/platform_update/', masters_apis.platform_update, name = 'platform_update'),
    path('api/all_platform_list/', masters_apis.all_platform_list, name = 'all_platform_list'),
    path('api/platform_delete_inactive/', masters_apis.platform_delete_inactive, name = 'platform_delete_inactive'),
    path('api/all_active_platform_list/', masters_apis.all_active_platform_list, name = 'all_active_platform_list'),


    ## Staff
    path('api/staff_register/', staff_apis.staff_register, name = 'staff_register'),
    path('api/list_all_staff/', staff_apis.list_all_staff, name = 'list_all_staff'),
    path('api/staff_status_update/', staff_apis.staff_status_update, name = 'staff_status_update'),
    path('api/staff_update/', staff_apis.staff_update, name = 'staff_update'),
    path('api/active_all_staff/', staff_apis.active_all_staff, name = 'active_all_staff'),
    path('api/list_only_staff/', staff_apis.list_only_staff, name = 'list_only_staff'),
    path('api/staff_profile_image_update/', staff_apis.staff_profile_image_update, name = 'staff_profile_image_update'),
    path('api/admin_staff_data_update_request/', staff_apis.admin_staff_data_update_request, name = 'admin_staff_data_update_request'),
    path('api/staff_module_rights/', staff_apis.staff_module_rights, name = 'staff_module_rights'),
    path('api/staff_module_update/', staff_apis.staff_module_update, name = 'staff_module_update'),
    path('api/staff_delete_inactive/', staff_apis.staff_delete_inactive, name = 'staff_delete_inactive'),
      
    ### Corporate
    path('api/corporate_register/', corporate_apis.corporate_register, name = 'corporate_register'),
    path('api/list_all_corporate/', corporate_apis.list_all_corporate, name = 'list_all_corporate'),
    path('api/corporate_update/', corporate_apis.corporate_update, name = 'corporate_update'),
    path('api/corporate_status_update/', corporate_apis.corporate_status_update, name = 'corporate_status_update'),
    path('api/active_all_corporate/', corporate_apis.active_all_corporate, name = 'active_all_corporate'),
    path('api/corporate_code_check/', corporate_apis.corporate_code_check, name = 'corporate_code_check'),
    path('api/corporate_package_list/', corporate_apis.corporate_package_list, name = 'corporate_package_list'),
    path('api/corporate_delete_inactive/', corporate_apis.corporate_delete_inactive, name = 'corporate_delete_inactive'),
    

    ### vendor
    path('api/vendor_register/', vendor_apis.vendor_register, name = 'vendor_register'),
    path('api/list_all_vendor/', vendor_apis.list_all_vendor, name = 'list_all_vendor'),
    path('api/vendor_update/', vendor_apis.vendor_update, name = 'vendor_update'),
    path('api/vendor_status_update/', vendor_apis.vendor_status_update, name = 'vendor_status_update'),
    path('api/all_active_vendor/', masters_apis.all_active_vendor, name = 'all_active_vendor'),
    path('api/vendor_code_check/', vendor_apis.vendor_code_check, name = 'vendor_code_check'),
    path('api/vendor_delete_inactive/', vendor_apis.vendor_delete_inactive, name = 'vendor_delete_inactive'),
    path('api/vendor_profile_image_update/', vendor_apis.vendor_profile_image_update, name = 'vendor_profile_image_update'),
    path('api/service_visit_wise_vendor_list/', vendor_apis.service_visit_wise_vendor_list, name = 'service_visit_wise_vendor_list'),
    path('api/service_wise_vendor_list/', vendor_apis.service_wise_vendor_list, name = 'service_wise_vendor_list'),
    
    
    
    ### Employee
    path('api/employee_register/', employee_apis.employee_register, name = 'employee_register'),
    path('api/employee_update/', employee_apis.employee_update, name = 'employee_update'),
    path('api/employee_status_update/', employee_apis.employee_status_update, name = 'employee_status_update'),
    path('api/list_all_employee/', employee_apis.list_all_employee, name = 'list_all_employee'),
    path('api/active_employee_list/', employee_apis.active_employee_list, name = 'active_employee_list'),
    path('api/employee_list_by_corporate/', corporate_apis.employee_list_by_corporate, name = 'employee_list_by_corporate'),
    path('api/employee_dependent_list/', employee_apis.employee_dependent_list, name = 'employee_dependent_list'),
    path('api/employee_data_update/', employee_apis.employee_data_update, name = 'employee_data_update'),
    path('api/new_employee_dependent_request/', employee_apis.new_employee_dependent_request, name = 'new_employee_dependent_request'),
    path('api/employee_profile_image_update/', employee_apis.employee_profile_image_update, name = 'employee_profile_image_update'),
    path('api/employee_delete_inactive/', employee_apis.employee_delete_inactive, name = 'employee_delete_inactive'),
    path('api/update_dependent_employee/', employee_apis.update_dependent_employee, name = 'update_dependent_employee'),
    path('api/employee_address_update/', employee_apis.employee_address_update, name = 'employee_address_update'),
    path('api/employee_address_create/', employee_apis.employee_address_create, name = 'employee_address_create'),
    path('api/employee_address_list/', employee_apis.employee_address_list, name = 'employee_address_list'),
    path('api/employee_address_delete/', employee_apis.employee_address_delete, name = 'employee_address_delete'),
    
    


    # ### Package
    path('api/package_create/', package_apis.package_create, name = 'package_create'),
    path('api/package_update/', package_apis.package_update, name = 'package_update'),
    path('api/package_status_update/', package_apis.package_status_update, name = 'package_status_update'),
    path('api/list_all_package/', package_apis.list_all_package, name = 'list_all_package'),
    path('api/all_active_package/', masters_apis.all_active_package, name = 'all_active_package'),
    path('api/service_wise_package_list_employee/', package_apis.service_wise_package_list_employee, name = 'service_wise_package_list_employee'),
    path('api/package_list_employee/', package_apis.package_list_employee, name = 'package_list_employee'),
    path('api/search_package/', package_apis.search_package, name = 'search_package'),
    path('api/package_delete_inactive/', package_apis.package_delete_inactive, name = 'package_delete_inactive'),
    path('api/service_wise_package_list_individual/', package_apis.service_wise_package_list_individual, name = 'service_wise_package_list_individual'),
    path('api/package_list_individual/', package_apis.package_list_individual, name = 'package_list_individual'),
    path('api/vendor_wise_package_list/', package_apis.vendor_wise_package_list, name = 'vendor_wise_package_list'),
    path('api/service_wise_package_list/', package_apis.service_wise_package_list, name = 'service_wise_package_list'),
    path('api/package_tests/', package_apis.package_tests, name = 'package_tests'),
    path('api/package_tests_update/', package_apis.package_tests_update, name = 'package_tests_update'),
    path('api/compare_package/', package_apis.compare_package, name = 'compare_package'),
    path('api/compare_package_list/', package_apis.compare_package_list, name = 'compare_package_list'),
    path('api/package_filter_list/', package_apis.package_filter_list, name = 'package_filter_list'),
    path('api/package_detail/', package_apis.package_detail, name = 'package_detail'),
    path('api/search_package_individual/', package_apis.search_package_individual, name = 'search_package_individual'),
    
    
    ## Website
    path('api/web_service_list/', package_apis.web_service_list, name = 'web_service_list'),
    path('api/web_package_list/', package_apis.web_package_list, name = 'web_package_list'),
    path('api/web_package_list_home/', package_apis.web_package_list_home, name = 'web_package_list_home'),

    ### Center
    path('api/center_create/', center_apis.center_create, name = 'center_create'),
    path('api/center_update/', center_apis.center_update, name = 'center_update'),
    path('api/center_status_update/', center_apis.center_status_update, name = 'center_status_update'),
    path('api/list_all_center/', center_apis.list_all_center, name = 'list_all_center'),
    path('api/center_serivce_list_by_vendor/', center_apis.center_serivce_list_by_vendor, name = 'center_serivce_list_by_vendor'),
    path('api/center_delete_inactive/', center_apis.center_delete_inactive, name = 'center_delete_inactive'),
    path('api/package_wise_center/', package_apis.package_wise_center, name = 'package_wise_center'),
    path('api/active_center_list/', center_apis.active_center_list, name = 'active_center_list'),
    
    
    ### Holiday
    path('api/holiday_create/', center_apis.holiday_create, name = 'holiday_create'),
    path('api/holiday_update/', center_apis.holiday_update, name = 'holiday_update'),
    path('api/holiday_status_update/', center_apis.holiday_status_update, name = 'holiday_status_update'),
    path('api/list_all_holiday/', center_apis.list_all_holiday, name = 'list_all_holiday'),
    path('api/holiday_delete_inactive/', center_apis.holiday_delete_inactive, name = 'holiday_delete_inactive'),
    path('api/center_holiday_list/', center_apis.center_holiday_list, name = 'center_holiday_list'),
    
    
    ### Health Tips
    path('api/health_tips_create/', engagement_apis.health_tips_create, name = 'health_tips_create'),
    path('api/health_tips_update/', engagement_apis.health_tips_update, name = 'health_tips_update'),
    path('api/health_tips_status_update/', engagement_apis.health_tips_status_update, name = 'health_tips_status_update'),
    path('api/list_all_health_tips/', engagement_apis.list_all_health_tips, name = 'list_all_health_tips'),
    path('api/list_active_health_tips/', engagement_apis.list_active_health_tips, name = 'list_active_health_tips'),
    path('api/active_inactive_health_tips/', engagement_apis.active_inactive_health_tips, name = 'active_inactive_health_tips'),
    path('api/health_tips_delete_inactive/', engagement_apis.health_tips_delete_inactive, name = 'health_tips_delete_inactive'),
    
    #### Appionment
    path('api/appointment_create/', appointment_apis.appointment_create, name = 'appointment_create'),
    path('api/all_appointment_list/', appointment_apis.all_appointment_list, name = 'all_appointment_list'),
    path('api/employee_appointment_list/', appointment_apis.employee_appointment_list, name = 'employee_appointment_list'),
    path('api/appointment_booking_reschedule/', appointment_apis.appointment_booking_reschedule, name = 'appointment_booking_reschedule'),
    path('api/reschedule_appointment_list/', appointment_apis.reschedule_appointment_list, name = 'reschedule_appointment_list'),
    path('api/appointment_list_for_vendor/', appointment_apis.appointment_list_for_vendor, name = 'appointment_list_for_vendor'),
    path('api/appointment_cancel_done/', appointment_apis.appointment_cancel_done, name = 'appointment_cancel_done'),
    path('api/appointment_delete_inactive/', appointment_apis.appointment_delete_inactive, name = 'appointment_delete_inactive'),
    path('api/appointment_data_check/', appointment_apis.appointment_data_check, name = 'appointment_data_check'),
    path('api/appointment_date_update/', appointment_apis.appointment_date_update, name = 'appointment_date_update'),
    path('api/add_to_card_transaction_create/', orders_billing_apis.add_to_card_transaction_create, name = 'add_to_card_transaction_create'),
    
    
    #### Bulk Import
    path('api/bulk_import/', employee_apis.bulk_import, name = 'bulk_import'),
    path('api/bulk_import_submit/', employee_apis.bulk_import_submit, name = 'bulk_import_submit'),


    ### Individual
    path('api/individual_register/', individual_apis.individual_register, name = 'individual_register'),
    path('api/individual_dependent_list/', individual_apis.individual_dependent_list, name = 'individual_dependent_list'),
    path('api/add_dependent_individual_employee/', individual_apis.add_dependent_individual_employee, name = 'add_dependent_individual_employee'),
    path('api/individual_appointment_list/', appointment_apis.individual_appointment_list, name = 'individual_appointment_list'),
    path('api/all_individual_list/', individual_apis.all_individual_list, name = 'all_individual_list'),
    path('api/individual_profile_image_update/', individual_apis.individual_profile_image_update, name = 'individual_profile_image_update'),
    path('api/individual_update/', individual_apis.individual_update, name = 'individual_update'),
    path('api/update_dependent_individual_employee/', individual_apis.update_dependent_individual_employee, name = 'update_dependent_individual_employee'),
    path('api/individual_status_update/', individual_apis.individual_status_update, name = 'individual_status_update'),
    path('api/individual_delete_inactive/', individual_apis.individual_delete_inactive, name = 'individual_delete_inactive'),
    path('api/individual_address_create/', individual_apis.individual_address_create, name = 'individual_address_create'),
    path('api/individual_address_update/', individual_apis.individual_address_update, name = 'individual_address_update'),
    path('api/individual_address_list/', individual_apis.individual_address_list, name = 'individual_address_list'),
    path('api/individual_address_delete/', individual_apis.individual_address_delete, name = 'individual_address_delete'),

    

    #### Redirect data
    path('api/redirect_login_wellness/', auth_apis.redirect_login_wellness, name = 'redirect_login_wellness'),
    path('api/give_access/', auth_apis.give_access, name = 'give_access'),
    
    
    path('api/encrypt_data/', auth_apis.encrypt_data, name = 'encrypt_data'),
    
    
    path('api/create_order_apiview/', orders_billing_apis.create_order_apiview, name = 'create_order_apiview'),
    path('api/verify_payment_apiview/', orders_billing_apis.verify_payment_apiview, name = 'verify_payment_apiview'),
    
    #### Offer 
    path('api/offer_create/', engagement_apis.offer_create, name = 'offer_create'),
    path('api/list_all_offer/', engagement_apis.list_all_offer, name = 'list_all_offer'),
    path('api/offer_update/', engagement_apis.offer_update, name = 'offer_update'),
    

    #### Notification 
    path('api/all_notification_user/', engagement_apis.all_notification_user, name = 'all_notification_user'),
    path('api/notification_detail/', engagement_apis.notification_detail, name = 'notification_detail'),
    
    #### Transaction
    path('api/all_transaction_list/', orders_billing_apis.all_transaction_list, name = 'all_transaction_list'),
    path('api/user_transaction_list/', orders_billing_apis.user_transaction_list, name = 'user_transaction_list'),
    
    
    path('api/tomorrow_check/', appointment_apis.tomorrow_check, name = 'tomorrow_check'),
    path('api/invoice_template/', orders_billing_apis.invoice_template, name = 'invoice_template'),
    
    ## ADD TO CART
    path('api/add_to_cart_create/', orders_billing_apis.add_to_cart_create, name = 'add_to_cart_create'),
    path('api/add_to_cart_list/', orders_billing_apis.add_to_cart_list, name = 'add_to_cart_list'),
    path('api/add_to_cart_delete/', orders_billing_apis.add_to_cart_delete, name = 'add_to_cart_delete'),
    path('api/add_to_cart_count/', orders_billing_apis.add_to_cart_count, name = 'add_to_cart_count'),


    path('api/user_data_svasthya/', orders_billing_apis.user_data_svasthya, name = 'user_data_svasthya'),
    path('api/employee_booking_list_svasthya/', employee_apis.employee_booking_list_svasthya, name = 'employee_booking_list_svasthya'),
    path('api/employee_booking_detail_svasthya/', employee_apis.employee_booking_detail_svasthya, name = 'employee_booking_detail_svasthya'),
    path('api/booking_list_svasthya/', orders_billing_apis.booking_list_svasthya, name = 'booking_list_svasthya'),


### TESTING
    path('api/center_list_testing_ebpf/', center_apis.center_list_testing_ebpf, name = 'center_list_testing_ebpf'),
    path('api/package_list_employee_test/', package_apis.package_list_employee_test, name = 'package_list_employee_test'),
    path('api/service_wise_package_list_employee_test/', package_apis.service_wise_package_list_employee_test, name = 'service_wise_package_list_employee_test'),
    path('api/service_wise_package_list_employee_test_two/', package_apis.service_wise_package_list_employee_test_two, name = 'service_wise_package_list_employee_test_two'),
    path('api/employee_to_individual_register/', employee_apis.employee_to_individual_register, name = 'employee_to_individual_register'),
    path('api/expiry_corporate_list/', corporate_apis.expiry_corporate_list, name = 'expiry_corporate_list'),


## Export
    path('api/package_export/', package_apis.package_export, name = 'package_export'),
    path('api/center_export/', center_apis.center_export, name = 'center_export'),
    path('api/appointment_export/', appointment_apis.appointment_export, name = 'appointment_export'),

    ### Test Category

    path('api/test_category_create/', masters_apis.test_category_create, name = 'test_category_create'),
    path('api/test_category_update/', masters_apis.test_category_update, name = 'test_category_update'),
    path('api/all_test_category_list/', masters_apis.all_test_category_list, name = 'all_test_category_list'),
    path('api/test_sub_category_create/', masters_apis.test_sub_category_create, name = 'test_sub_category_create'),
    path('api/test_sub_category_update/', masters_apis.test_sub_category_update, name = 'test_sub_category_update'),
    path('api/all_test_subcategory_list/', masters_apis.all_test_subcategory_list, name = 'all_test_subcategory_list'),
    path('api/test_category_delete_inactive/', masters_apis.test_category_delete_inactive, name = 'test_category_delete_inactive'),
    path('api/all_active_test_category_list/', masters_apis.all_active_test_category_list, name = 'all_active_test_category_list'),
    path('api/test_sub_category_delete_inactive/', masters_apis.test_sub_category_delete_inactive, name = 'test_sub_category_delete_inactive'),
    path('api/all_active_test_subcategory_list/', masters_apis.all_active_test_subcategory_list, name = 'all_active_test_subcategory_list'),


    path('api/employee_address_create_temp/', employee_apis.employee_address_create_temp, name = 'employee_address_create_temp'),
    path('api/lat_long_test/', center_apis.lat_long_test, name = 'lat_long_test'),
    path('api/service_wise_package_list_employee_check/', package_apis.service_wise_package_list_employee_check, name = 'service_wise_package_list_employee_check'),
    path('api/service_wise_package_list_individual_check/', package_apis.service_wise_package_list_individual_check, name = 'service_wise_package_list_individual_check'),
    path('api/package_filter_list_check/', package_apis.package_filter_list_check, name = 'package_filter_list_check'),
    path('api/package_detail_slug/<slug:slug>/', package_apis.package_detail_slug, name = 'package_detail_slug'),
    
    # DARWINBOX & HOH PRE-EMPLOYMENT APIS (svasthyapp/apis/)
    path("api/darwinbox/report-data/", darwinbox_sync.darwinbox_report_data, name="darwinbox-report-data"),
    path("api/darwinbox/import-data/", darwinbox_sync.darwinbox_import_data, name="darwinbox-import-data"),
    path("api/all_hoh_employee_list/", hoh_employee.all_hoh_employee_list, name="all_hoh_employee_list"),
    path("api/hoh-employee-detail/", hoh_employee.get_hoh_employee_detail, name="get_hoh_employee_detail"),
    path("api/hoh_employee_detail/", hoh_employee.get_hoh_employee_detail, name="get_hoh_employee_detail_underscore"),
    path("api/hoh-employee-status-update/", hoh_employee.hoh_employee_status_update, name="hoh_employee_status_update"),
    path("api/hoh_employee_status_update/", hoh_employee.hoh_employee_status_update, name="hoh_employee_status_update_underscore"),
    path("api/hoh-employee-update/", hoh_employee.hoh_employee_status_update, name="hoh_employee_update"),
    path("api/hoh_employee_update/", hoh_employee.hoh_employee_status_update, name="hoh_employee_update_underscore"),
    path("api/center_list_hoh/", hoh_employee.vendor_center_list_hoh, name="vendor_center_list_hoh"),
    
    path('api/darwinbox/candidate-appointment-create/', candidate_appointments.darwinbox_candidate_appointment_create, name='darwinbox_candidate_appointment_create'),
    path('api/darwinbox/candidate-appointment-update/', candidate_appointments.darwinbox_candidate_appointment_update, name='darwinbox_candidate_appointment_update'),
    path('api/darwinbox/candidate-appointment-list/', candidate_appointments.all_darwinbox_candidate_appointment_list, name='all_darwinbox_candidate_appointment_list'),
    path('api/darwinbox/candidate-appointment-detail/', candidate_appointments.get_darwinbox_candidate_appointment_detail, name='get_darwinbox_candidate_appointment_detail'),
    path('api/darwinbox/candidate-appointment-data-check/', candidate_appointments.darwinbox_candidate_appointment_data_check, name='darwinbox_candidate_appointment_data_check'),
    path('api/darwinbox/candidate-appointment-delete/', candidate_appointments.delete_darwinbox_candidate_appointment, name='delete_darwinbox_candidate_appointment'),
    path('api/darwinbox/candidate-appointment-cancel-done/', candidate_appointments.darwinbox_candidate_appointment_cancel_done, name='darwinbox_candidate_appointment_cancel_done'),
    path('api/darwinbox/candidate-appointment-report-upload/', candidate_appointments.darwinbox_candidate_appointment_report_upload, name='darwinbox_candidate_appointment_report_upload'),
    path('api/darwinbox/candidate-appointment-booking-reschedule/', candidate_appointments.darwinbox_candidate_appointment_booking_reschedule, name='darwinbox_candidate_appointment_booking_reschedule'),
    path('api/darwinbox/candidate-appointment-reschedule/', candidate_appointments.darwinbox_candidate_appointment_reschedule, name='darwinbox_candidate_appointment_reschedule'),
    path('api/darwinbox/candidate-appointment-date-update/', candidate_appointments.darwinbox_candidate_appointment_date_update, name='darwinbox_candidate_appointment_date_update'),
    path('api/darwinbox/candidate-appointment-reschedule-list/', candidate_appointments.reschedule_darwinbox_candidate_appointment_list, name='reschedule_darwinbox_candidate_appointment_list'),
    path('api/reschedule_darwinbox_candidate_appointment_list/', candidate_appointments.reschedule_darwinbox_candidate_appointment_list, name='reschedule_darwinbox_candidate_appointment_list_direct'),
    path('api/darwinbox/candidate-appointment-full-manage/', candidate_appointments.darwinbox_candidate_appointment_full_manage, name='darwinbox_candidate_appointment_full_manage'),

    path('api/address_select_update/', orders_billing_apis.address_select_update, name = 'address_select_update'),
    path('api/swagger-endpoints/', swagger.api_endpoints_catalog, name = 'api_endpoints_catalog'),
    path('api/swagger/', swagger.schema_view.with_ui('swagger', cache_timeout=0), name = 'api_swagger_ui'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
