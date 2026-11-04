from django.urls import path
from svasthyapp import views, swagger

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
    path('api/staff_department_delete_inactive/', views.staff_department_delete_inactive, name = 'staff_department_delete_inactive'),

    ## Type OF access
    path('api/type_of_access_create/', views.type_of_access_create, name = 'type_of_access_create'),
    path('api/type_of_access_update/', views.type_of_access_update, name = 'type_of_access_update'),
    path('api/all_type_of_access_list/', views.all_type_of_access_list, name = 'all_type_of_access_list'),
    path('api/all_active_type_of_access_list/', views.all_active_type_of_access_list, name = 'all_active_type_of_access_list'),
    path('api/type_of_access_delete_inactive/', views.type_of_access_delete_inactive, name = 'type_of_access_delete_inactive'),

    ## Staff Level
    path('api/staff_level_create/', views.staff_level_create, name = 'staff_level_create'),
    path('api/staff_level_update/', views.staff_level_update, name = 'staff_level_update'),
    path('api/all_staff_level_list/', views.all_staff_level_list, name = 'all_staff_level_list'),
    path('api/all_active_staff_level_list/', views.all_active_staff_level_list, name = 'all_active_staff_level_list'),
    path('api/staff_level_delete_inactive/', views.staff_level_delete_inactive, name = 'staff_level_delete_inactive'),

    ## Staff Type
    path('api/staff_type_create/', views.staff_type_create, name = 'staff_type_create'),
    path('api/staff_type_update/', views.staff_type_update, name = 'staff_type_update'),
    path('api/all_staff_type_list/', views.all_staff_type_list, name = 'all_staff_type_list'),
    path('api/all_active_staff_type_list/', views.all_active_staff_type_list, name = 'all_active_staff_type_list'),
    path('api/staff_type_delete_inactive/', views.staff_type_delete_inactive, name = 'staff_type_delete_inactive'),

    ## Age Category
    path('api/age_category_create/', views.age_category_create, name = 'age_category_create'),
    path('api/age_category_update/', views.age_category_update, name = 'age_category_update'),
    path('api/all_age_category_list/', views.all_age_category_list, name = 'all_age_category_list'),
    path('api/all_active_age_category_list/', views.all_active_age_category_list, name = 'all_active_age_category_list'),
    path('api/age_category_delete_inactive/', views.age_category_delete_inactive, name = 'age_category_delete_inactive'),

    ## Gender
    path('api/gender_create/', views.gender_create, name = 'gender_create'),
    path('api/gender_update/', views.gender_update, name = 'gender_update'),
    path('api/all_gender_list/', views.all_gender_list, name = 'all_gender_list'),
    path('api/all_active_gender_list/', views.all_active_gender_list, name = 'all_active_gender_list'),
    path('api/gender_delete_inactive/', views.gender_delete_inactive, name = 'gender_delete_inactive'),

    ## Relation
    path('api/relation_create/', views.relation_create, name = 'relation_create'),
    path('api/relation_update/', views.relation_update, name = 'relation_update'),
    path('api/all_relation_list/', views.all_relation_list, name = 'all_relation_list'),
    path('api/all_active_relation_list/', views.all_active_relation_list, name = 'all_active_relation_list'),
    path('api/relation_delete_inactive/', views.relation_delete_inactive, name = 'relation_delete_inactive'),

    ## Type of Service 
    path('api/type_of_service_create/', views.type_of_service_create, name = 'type_of_service_create'),
    path('api/type_of_service_update/', views.type_of_service_update, name = 'type_of_service_update'),
    path('api/all_type_of_service_list/', views.all_type_of_service_list, name = 'all_type_of_service_list'),
    path('api/all_active_type_of_service_list/', views.all_active_type_of_service_list, name = 'all_active_type_of_service_list'),
    path('api/type_of_service_delete_inactive/', views.type_of_service_delete_inactive, name = 'type_of_service_delete_inactive'),

    ## Type of Visit 
    path('api/type_of_visit_create/', views.type_of_visit_create, name = 'type_of_visit_create'),
    path('api/type_of_visit_update/', views.type_of_visit_update, name = 'type_of_visit_update'),
    path('api/all_type_of_visit_list/', views.all_type_of_visit_list, name = 'all_type_of_visit_list'),
    path('api/all_active_type_of_visit_list/', views.all_active_type_of_visit_list, name = 'all_active_type_of_visit_list'),
    path('api/type_of_visit_delete_inactive/', views.type_of_visit_delete_inactive, name = 'type_of_visit_delete_inactive'),

    ## Parent Company
    path('api/parent_company_create/', views.parent_company_create, name = 'parent_company_create'),
    path('api/parent_company_update/', views.parent_company_update, name = 'parent_company_update'),
    path('api/all_parent_company_list/', views.all_parent_company_list, name = 'all_parent_company_list'),
    path('api/all_active_parent_company_list/', views.all_active_parent_company_list, name = 'all_active_parent_company_list'),
    path('api/parent_company_delete_inactive/', views.parent_company_delete_inactive, name = 'parent_company_delete_inactive'),


    ## Billing Cycle 
    path('api/billing_cycle_create/', views.billing_cycle_create, name = 'billing_cycle_create'),
    path('api/billing_cycle_update/', views.billing_cycle_update, name = 'billing_cycle_update'),
    path('api/all_billing_cycle_list/', views.all_billing_cycle_list, name = 'all_billing_cycle_list'),
    path('api/all_active_billing_cycle_list/', views.all_active_billing_cycle_list, name = 'all_active_billing_cycle_list'),
    path('api/billing_cycle_delete_inactive/', views.billing_cycle_delete_inactive, name = 'billing_cycle_delete_inactive'),

    ## Weekdays
    path('api/weekdays_create/', views.weekdays_create, name = 'weekdays_create'),
    path('api/weekdays_update/', views.weekdays_update, name = 'weekdays_update'),
    path('api/all_weekdays_list/', views.all_weekdays_list, name = 'all_weekdays_list'),
    path('api/all_active_weekdays_list/', views.all_active_weekdays_list, name = 'all_active_weekdays_list'),
    path('api/weekdays_delete_inactive/', views.weekdays_delete_inactive, name = 'weekdays_delete_inactive'),

    ## Holidays
    path('api/holidays_create/', views.holidays_create, name = 'holidays_create'),
    path('api/holidays_update/', views.holidays_update, name = 'holidays_update'),
    path('api/all_holidays_list/', views.all_holidays_list, name = 'all_holidays_list'),
    path('api/all_active_holidays_list/', views.all_active_holidays_list, name = 'all_active_holidays_list'),
    path('api/holidays_delete_inactive/', views.holidays_delete_inactive, name = 'holidays_delete_inactive'),

    ## Payment Tags
    path('api/payment_tags_create/', views.payment_tags_create, name = 'payment_tags_create'),
    path('api/payment_tags_update/', views.payment_tags_update, name = 'payment_tags_update'),
    path('api/all_payment_tags_list/', views.all_payment_tags_list, name = 'all_payment_tags_list'),
    path('api/all_active_payment_tags_list/', views.all_active_payment_tags_list, name = 'all_active_payment_tags_list'),
    path('api/payment_tags_delete_inactive/', views.payment_tags_delete_inactive, name = 'payment_tags_delete_inactive'),
    
    ## Type of industry
    path('api/type_of_industry_create/', views.type_of_industry_create, name = 'type_of_industry_create'),
    path('api/type_of_industry_update/', views.type_of_industry_update, name = 'type_of_industry_update'),
    path('api/all_type_of_industry_list/', views.all_type_of_industry_list, name = 'all_type_of_industry_list'),
    path('api/all_active_type_of_industry_list/', views.all_active_type_of_industry_list, name = 'all_active_type_of_industry_list'),
    path('api/type_of_industry_delete_inactive/', views.type_of_industry_delete_inactive, name = 'type_of_industry_delete_inactive'),

    ## Duration
    path('api/duration_create/', views.duration_create, name = 'duration_create'),
    path('api/duration_update/', views.duration_update, name = 'duration_update'),
    path('api/all_duration_list/', views.all_duration_list, name = 'all_duration_list'),
    path('api/all_active_duration_list/', views.all_active_duration_list, name = 'all_active_duration_list'),
    path('api/duration_delete_inactive/', views.duration_delete_inactive, name = 'duration_delete_inactive'),

    ## Platform
    path('api/platform_create/', views.platform_create, name = 'platform_create'),
    path('api/platform_update/', views.platform_update, name = 'platform_update'),
    path('api/all_platform_list/', views.all_platform_list, name = 'all_platform_list'),
    path('api/platform_delete_inactive/', views.platform_delete_inactive, name = 'platform_delete_inactive'),
    path('api/all_active_platform_list/', views.all_active_platform_list, name = 'all_active_platform_list'),


    ## Staff
    path('api/staff_register/', views.staff_register, name = 'staff_register'),
    path('api/list_all_staff/', views.list_all_staff, name = 'list_all_staff'),
    path('api/staff_status_update/', views.staff_status_update, name = 'staff_status_update'),
    path('api/staff_update/', views.staff_update, name = 'staff_update'),
    path('api/active_all_staff/', views.active_all_staff, name = 'active_all_staff'),
    path('api/list_only_staff/', views.list_only_staff, name = 'list_only_staff'),
    path('api/staff_profile_image_update/', views.staff_profile_image_update, name = 'staff_profile_image_update'),
    path('api/admin_staff_data_update_request/', views.admin_staff_data_update_request, name = 'admin_staff_data_update_request'),
    path('api/staff_module_rights/', views.staff_module_rights, name = 'staff_module_rights'),
    path('api/staff_module_update/', views.staff_module_update, name = 'staff_module_update'),
    path('api/staff_delete_inactive/', views.staff_delete_inactive, name = 'staff_delete_inactive'),
      
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
    path('api/service_visit_wise_vendor_list/', views.service_visit_wise_vendor_list, name = 'service_visit_wise_vendor_list'),
    path('api/service_wise_vendor_list/', views.service_wise_vendor_list, name = 'service_wise_vendor_list'),
    
    
    
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
    path('api/update_dependent_employee/', views.update_dependent_employee, name = 'update_dependent_employee'),
    path('api/employee_address_update/', views.employee_address_update, name = 'employee_address_update'),
    path('api/employee_address_create/', views.employee_address_create, name = 'employee_address_create'),
    path('api/employee_address_list/', views.employee_address_list, name = 'employee_address_list'),
    path('api/employee_address_delete/', views.employee_address_delete, name = 'employee_address_delete'),
    
    


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
    path('api/service_wise_package_list_individual/', views.service_wise_package_list_individual, name = 'service_wise_package_list_individual'),
    path('api/package_list_individual/', views.package_list_individual, name = 'package_list_individual'),
    path('api/vendor_wise_package_list/', views.vendor_wise_package_list, name = 'vendor_wise_package_list'),
    path('api/service_wise_package_list/', views.service_wise_package_list, name = 'service_wise_package_list'),
    path('api/package_tests/', views.package_tests, name = 'package_tests'),
    path('api/package_tests_update/', views.package_tests_update, name = 'package_tests_update'),
    path('api/compare_package/', views.compare_package, name = 'compare_package'),
    path('api/compare_package_list/', views.compare_package_list, name = 'compare_package_list'),
    path('api/package_filter_list/', views.package_filter_list, name = 'package_filter_list'),
    path('api/package_detail/', views.package_detail, name = 'package_detail'),
    path('api/search_package_individual/', views.search_package_individual, name = 'search_package_individual'),
    
    
    ## Website
    path('api/web_service_list/', views.web_service_list, name = 'web_service_list'),
    path('api/web_package_list/', views.web_package_list, name = 'web_package_list'),
    path('api/web_package_list_home/', views.web_package_list_home, name = 'web_package_list_home'),

    ### Center
    path('api/center_create/', views.center_create, name = 'center_create'),
    path('api/center_update/', views.center_update, name = 'center_update'),
    path('api/center_status_update/', views.center_status_update, name = 'center_status_update'),
    path('api/list_all_center/', views.list_all_center, name = 'list_all_center'),
    path('api/center_serivce_list_by_vendor/', views.center_serivce_list_by_vendor, name = 'center_serivce_list_by_vendor'),
    path('api/center_delete_inactive/', views.center_delete_inactive, name = 'center_delete_inactive'),
    path('api/package_wise_center/', views.package_wise_center, name = 'package_wise_center'),
    path('api/active_center_list/', views.active_center_list, name = 'active_center_list'),
    
    
    ### Holiday
    path('api/holiday_create/', views.holiday_create, name = 'holiday_create'),
    path('api/holiday_update/', views.holiday_update, name = 'holiday_update'),
    path('api/holiday_status_update/', views.holiday_status_update, name = 'holiday_status_update'),
    path('api/list_all_holiday/', views.list_all_holiday, name = 'list_all_holiday'),
    path('api/holiday_delete_inactive/', views.holiday_delete_inactive, name = 'holiday_delete_inactive'),
    path('api/center_holiday_list/', views.center_holiday_list, name = 'center_holiday_list'),
    
    
    ### Health Tips
    path('api/health_tips_create/', views.health_tips_create, name = 'health_tips_create'),
    path('api/health_tips_update/', views.health_tips_update, name = 'health_tips_update'),
    path('api/health_tips_status_update/', views.health_tips_status_update, name = 'health_tips_status_update'),
    path('api/list_all_health_tips/', views.list_all_health_tips, name = 'list_all_health_tips'),
    path('api/list_active_health_tips/', views.list_active_health_tips, name = 'list_active_health_tips'),
    path('api/active_inactive_health_tips/', views.active_inactive_health_tips, name = 'active_inactive_health_tips'),
    path('api/health_tips_delete_inactive/', views.health_tips_delete_inactive, name = 'health_tips_delete_inactive'),
    
    #### Appionment
    path('api/appointment_create/', views.appointment_create, name = 'appointment_create'),
    path('api/all_appointment_list/', views.all_appointment_list, name = 'all_appointment_list'),
    path('api/employee_appointment_list/', views.employee_appointment_list, name = 'employee_appointment_list'),
    path('api/appointment_booking_reschedule/', views.appointment_booking_reschedule, name = 'appointment_booking_reschedule'),
    path('api/reschedule_appointment_list/', views.reschedule_appointment_list, name = 'reschedule_appointment_list'),
    path('api/appointment_list_for_vendor/', views.appointment_list_for_vendor, name = 'appointment_list_for_vendor'),
    path('api/appointment_cancel_done/', views.appointment_cancel_done, name = 'appointment_cancel_done'),
    path('api/appointment_delete_inactive/', views.appointment_delete_inactive, name = 'appointment_delete_inactive'),
    path('api/appointment_data_check/', views.appointment_data_check, name = 'appointment_data_check'),
    path('api/appointment_date_update/', views.appointment_date_update, name = 'appointment_date_update'),
    path('api/add_to_card_transaction_create/', views.add_to_card_transaction_create, name = 'add_to_card_transaction_create'),
    
    
    #### Bulk Import
    path('api/bulk_import/', views.bulk_import, name = 'bulk_import'),
    path('api/bulk_import_submit/', views.bulk_import_submit, name = 'bulk_import_submit'),


    ### Individual
    path('api/individual_register/', views.individual_register, name = 'individual_register'),
    path('api/individual_dependent_list/', views.individual_dependent_list, name = 'individual_dependent_list'),
    path('api/add_dependent_individual_employee/', views.add_dependent_individual_employee, name = 'add_dependent_individual_employee'),
    path('api/individual_appointment_list/', views.individual_appointment_list, name = 'individual_appointment_list'),
    path('api/all_individual_list/', views.all_individual_list, name = 'all_individual_list'),
    path('api/individual_profile_image_update/', views.individual_profile_image_update, name = 'individual_profile_image_update'),
    path('api/individual_update/', views.individual_update, name = 'individual_update'),
    path('api/update_dependent_individual_employee/', views.update_dependent_individual_employee, name = 'update_dependent_individual_employee'),
    path('api/individual_status_update/', views.individual_status_update, name = 'individual_status_update'),
    path('api/individual_delete_inactive/', views.individual_delete_inactive, name = 'individual_delete_inactive'),
    path('api/individual_address_create/', views.individual_address_create, name = 'individual_address_create'),
    path('api/individual_address_update/', views.individual_address_update, name = 'individual_address_update'),
    path('api/individual_address_list/', views.individual_address_list, name = 'individual_address_list'),
    path('api/individual_address_delete/', views.individual_address_delete, name = 'individual_address_delete'),

    

    #### Redirect data
    path('api/redirect_login_wellness/', views.redirect_login_wellness, name = 'redirect_login_wellness'),
    path('api/give_access/', views.give_access, name = 'give_access'),
    
    
    path('api/encrypt_data/', views.encrypt_data, name = 'encrypt_data'),
    
    
    path('api/create_order_apiview/', views.create_order_apiview, name = 'create_order_apiview'),
    path('api/verify_payment_apiview/', views.verify_payment_apiview, name = 'verify_payment_apiview'),
    
    #### Offer 
    path('api/offer_create/', views.offer_create, name = 'offer_create'),
    path('api/list_all_offer/', views.list_all_offer, name = 'list_all_offer'),
    path('api/offer_update/', views.offer_update, name = 'offer_update'),
    

    #### Notification 
    path('api/all_notification_user/', views.all_notification_user, name = 'all_notification_user'),
    path('api/notification_detail/', views.notification_detail, name = 'notification_detail'),
    
    #### Transaction
    path('api/all_transaction_list/', views.all_transaction_list, name = 'all_transaction_list'),
    path('api/user_transaction_list/', views.user_transaction_list, name = 'user_transaction_list'),
    
    
    path('api/tomorrow_check/', views.tomorrow_check, name = 'tomorrow_check'),
    path('api/invoice_template/', views.invoice_template, name = 'invoice_template'),
    
    ## ADD TO CART
    path('api/add_to_cart_create/', views.add_to_cart_create, name = 'add_to_cart_create'),
    path('api/add_to_cart_list/', views.add_to_cart_list, name = 'add_to_cart_list'),
    path('api/add_to_cart_delete/', views.add_to_cart_delete, name = 'add_to_cart_delete'),
    path('api/add_to_cart_count/', views.add_to_cart_count, name = 'add_to_cart_count'),


    path('api/user_data_svasthya/', views.user_data_svasthya, name = 'user_data_svasthya'),
    path('api/employee_booking_list_svasthya/', views.employee_booking_list_svasthya, name = 'employee_booking_list_svasthya'),
    path('api/employee_booking_detail_svasthya/', views.employee_booking_detail_svasthya, name = 'employee_booking_detail_svasthya'),
    path('api/booking_list_svasthya/', views.booking_list_svasthya, name = 'booking_list_svasthya'),


### TESTING
    path('api/center_list_testing_ebpf/', views.center_list_testing_ebpf, name = 'center_list_testing_ebpf'),
    path('api/package_list_employee_test/', views.package_list_employee_test, name = 'package_list_employee_test'),
    path('api/service_wise_package_list_employee_test/', views.service_wise_package_list_employee_test, name = 'service_wise_package_list_employee_test'),
    path('api/service_wise_package_list_employee_test_two/', views.service_wise_package_list_employee_test_two, name = 'service_wise_package_list_employee_test_two'),
    path('api/employee_to_individual_register/', views.employee_to_individual_register, name = 'employee_to_individual_register'),
    path('api/expiry_corporate_list/', views.expiry_corporate_list, name = 'expiry_corporate_list'),


## Export
    path('api/package_export/', views.package_export, name = 'package_export'),
    path('api/center_export/', views.center_export, name = 'center_export'),
    path('api/appointment_export/', views.appointment_export, name = 'appointment_export'),

    ### Test Category

    path('api/test_category_create/', views.test_category_create, name = 'test_category_create'),
    path('api/test_category_update/', views.test_category_update, name = 'test_category_update'),
    path('api/all_test_category_list/', views.all_test_category_list, name = 'all_test_category_list'),
    path('api/test_sub_category_create/', views.test_sub_category_create, name = 'test_sub_category_create'),
    path('api/test_sub_category_update/', views.test_sub_category_update, name = 'test_sub_category_update'),
    path('api/all_test_subcategory_list/', views.all_test_subcategory_list, name = 'all_test_subcategory_list'),
    path('api/test_category_delete_inactive/', views.test_category_delete_inactive, name = 'test_category_delete_inactive'),
    path('api/all_active_test_category_list/', views.all_active_test_category_list, name = 'all_active_test_category_list'),
    path('api/test_sub_category_delete_inactive/', views.test_sub_category_delete_inactive, name = 'test_sub_category_delete_inactive'),
    path('api/all_active_test_subcategory_list/', views.all_active_test_subcategory_list, name = 'all_active_test_subcategory_list'),


    path('api/employee_address_create_temp/', views.employee_address_create_temp, name = 'employee_address_create_temp'),
    path('api/lat_long_test/', views.lat_long_test, name = 'lat_long_test'),
    path('api/service_wise_package_list_employee_check/', views.service_wise_package_list_employee_check, name = 'service_wise_package_list_employee_check'),
    path('api/service_wise_package_list_individual_check/', views.service_wise_package_list_individual_check, name = 'service_wise_package_list_individual_check'),
    path('api/package_filter_list_check/', views.package_filter_list_check, name = 'package_filter_list_check'),
    path('api/package_detail_slug/<slug:slug>/', views.package_detail_slug, name = 'package_detail_slug'),
    
    path("api/darwinbox/report-data/",views.darwinbox_report_data,name="darwinbox-report-data"),
    path("api/darwinbox/import-data/",views.darwinbox_import_data,name="darwinbox-import-data"),
    path("api/all_hoh_employee_list/",views.all_hoh_employee_list,name="all_hoh_employee_list"),
    
    path('api/darwinbox/candidate-appointment-create/', views.darwinbox_candidate_appointment_create, name='darwinbox_candidate_appointment_create'),
    path('api/darwinbox/candidate-appointment-update/', views.darwinbox_candidate_appointment_update, name='darwinbox_candidate_appointment_update'),
    path('api/darwinbox/candidate-appointment-list/', views.all_darwinbox_candidate_appointment_list, name='all_darwinbox_candidate_appointment_list'),
    path('api/darwinbox/candidate-appointment-detail/', views.get_darwinbox_candidate_appointment_detail, name='get_darwinbox_candidate_appointment_detail'),
    path('api/darwinbox/candidate-appointment-data-check/', views.darwinbox_candidate_appointment_data_check, name='darwinbox_candidate_appointment_data_check'),
    path('api/darwinbox/candidate-appointment-delete/', views.delete_darwinbox_candidate_appointment, name='delete_darwinbox_candidate_appointment'),
    path('api/darwinbox/candidate-appointment-cancel-done/', views.darwinbox_candidate_appointment_cancel_done, name='darwinbox_candidate_appointment_cancel_done'),
    path('api/darwinbox/candidate-appointment-report-upload/', views.darwinbox_candidate_appointment_report_upload, name='darwinbox_candidate_appointment_report_upload'),
    path('api/darwinbox/candidate-appointment-booking-reschedule/', views.darwinbox_candidate_appointment_booking_reschedule, name='darwinbox_candidate_appointment_booking_reschedule'),
    path('api/darwinbox/candidate-appointment-reschedule/', views.darwinbox_candidate_appointment_reschedule, name='darwinbox_candidate_appointment_reschedule'),
    path('api/darwinbox/candidate-appointment-date-update/', views.darwinbox_candidate_appointment_date_update, name='darwinbox_candidate_appointment_date_update'),
    path('api/darwinbox/candidate-appointment-reschedule-list/', views.reschedule_darwinbox_candidate_appointment_list, name='reschedule_darwinbox_candidate_appointment_list'),
    path('api/reschedule_darwinbox_candidate_appointment_list/', views.reschedule_darwinbox_candidate_appointment_list, name='reschedule_darwinbox_candidate_appointment_list_direct'),
    path('api/darwinbox/candidate-appointment-full-manage/', views.darwinbox_candidate_appointment_full_manage, name='darwinbox_candidate_appointment_full_manage'),

    path('api/address_select_update/', views.address_select_update, name = 'address_select_update'),
    path('api/swagger-endpoints/', swagger.api_endpoints_catalog, name = 'api_endpoints_catalog'),
    path('api/swagger/', swagger.schema_view.with_ui('swagger', cache_timeout=0), name = 'api_swagger_ui'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
