from svasthyapp.apis.base import *
from svasthyapp.models import appointment_models

@csrf_exempt
def appointment_data_check(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        employee = python_data.get('employee')
        patient = python_data.get('patient')
        package = python_data.get('package')
        
        get_package_payment_tags = models.PackageDetail.objects.filter(id = package).values_list('tags', flat=True)[0]
        package_payment_tags = models.PaymentTags.objects.filter(id = get_package_payment_tags).values_list('payment_tags', flat=True)[0]
        
        if package_payment_tags == 'Corporate pay':
            check_appointment = models.AppointmentDetail.objects.filter(package =package, employee =employee, patient= patient).exclude(status='add_to_cart').count()
            if check_appointment != 0:
                check_booking = models.AppointmentDetail.objects.filter(package =package, employee =employee, patient= patient).exclude(status='Cancel').count()
                if check_booking == 1:
                    check_booking = models.AppointmentDetail.objects.filter(package =package, employee =employee, patient= patient).values_list('report', flat=True)[0]
                    if check_booking != None and check_booking != 'null' and check_booking != '':
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'first_time':False,
                            'package_book':True,
                            'is_self_pay':False,
                            'message' : "Health checkup benefit already utilised. Kindly explore other available packages"
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'package_book':True,
                            'is_self_pay':False,
                            'first_time':False,
                            'message' : "Appointment already booked and is currently under process"
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')
                else:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'package_book':False,
                        'is_self_pay':False,
                        'first_time':True,
                        'message' : "You're eligible for book this appointment."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
            elif check_appointment == 0:
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'package_book':False,
                    'is_self_pay':False,
                    'first_time':True,
                    'message' : "You're eligible for book this appointment."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 

        elif package_payment_tags == 'Self Pay':                            
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'first_time':False,
                    'is_self_pay':True,
                    'package_book':True,
                    'message' : "You need to pay by your self."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 

        else:

            res = {
                'statuscode' : 406,
                'status':False,
                'message' : "Something went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def appointment_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        individual = python_data.get('individual')
        employee = python_data.get('employee')
        patient = python_data.get('patient')
        package = python_data.get('package')
        center = python_data.get('center')
        appointment_date_1 = python_data.get('appointment_date_1', None)
        appointment_date_2 = python_data.get('appointment_date_2', None)
        home_sample_date_1 = python_data.get('home_sample_date_1', None)
        home_sample_date_2 = python_data.get('home_sample_date_2', None)
        flag = python_data.get('flag', 'employee')
        cart_flag = python_data.get('cart_flag')
        is_payment = python_data.get('is_payment')
        method = python_data.get('method')
        transaction_id = python_data.get('transaction_id')
        address = python_data.get('address')


        type_of_visit = models.PackageDetail.objects.filter(id = package).values_list('type_of_visit', flat=True)[0]

        now = datetime.now()
        formatted_date = now.strftime("%B %d, %Y")
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        curr_time = time.strftime("%H:%M:%S", time.localtime())
        current_time = now.strftime("%Y%m%d%H%M%S")
        current_date_booking = now.strftime("%Y%m%d")
        if cart_flag == True:
            status = 'add_to_cart'
        else: 
            status = 'Request Received'

        if flag == 'employee':
            check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
            list_data = []
            if check_employee == 1:
                vendor_id = models.PackageDetail.objects.filter(id = package).values_list('vendor', flat=True)[0]
                appointment_check = models.AppointmentDetail.objects.filter(employee_id = employee, patient_id = patient,package_id = package, status= 'add_to_cart').count()

                if appointment_check == 0 or appointment_check == 0:

                    appointment_create = models.AppointmentDetail.objects.create(
                        employee_id = employee,  
                        appointment_type = 'Employee',
                        patient_id = patient,
                        employee_address_id = address,
                        package_id = package,
                        center_id = center,
                        vendor_id = vendor_id,
                        type_of_visit_id = type_of_visit,
                        appointment_date_1 = appointment_date_1, 
                        appointment_date_2 = appointment_date_2,
                        home_sample_date_1 = home_sample_date_1,
                        home_sample_date_2 = home_sample_date_2,
                        status = status,
                        created_at = current_date
                    )
                    appointment_create.save()
                    appointment_id = appointment_create.id

                    if cart_flag != True:
                        package_data = models.PackageDetail.objects.get(id = package)
                        package_type = package_data.package_type
                        amount = package_data.offer_price
                        corporate_id = models.EmployeeDetail.objects.filter(id = employee).values_list('corporate', flat=True)[0]

                        if is_payment == False:
                            amount = 0
                        ### Invoice Data
                        total_today_appointment = models.AppointmentDetail.objects.filter(created_at =current_date).count()
                        formatted_num = format(total_today_appointment, '03d')
                        all_appointment = models.AppointmentDetail.objects.all().count()
                        all_formatted_num = format(all_appointment, '05d')
                        
                        booking_id = 'BKG-' + str(current_date_booking) + '-' +str(formatted_num)
                        
                        invoice_id = f'25-26/{formatted_num}/IN-{all_formatted_num}'
                        # 25-26/0001/IN-00001
                        transaction_create = models.Transaction.objects.create(
                            transaction_type = package_type,
                            appointment_id = appointment_create.id,
                            is_payment = is_payment,
                            booking_id = booking_id,
                            method = method,
                            transaction_id = transaction_id,
                            invoice_id = invoice_id,
                            individual_id=None,
                            corporate_id=corporate_id,
                            employee_id=employee,
                            package_id=package,
                            amount=amount,
                            patient_id = patient,
                            status='Paid',
                            reason = 'Paid but Appointment/Report is pending.',
                            created_at=current_date
                        ).save()

                        notification = models.NotificationDetail.objects.create(
                            title = 'Health Checkup Request Received',
                            notification_type = 'Acknowledgment',
                            preferred_appointment_date1 = appointment_date_1,
                            preferred_appointment_date2 = appointment_date_2,
                            user_type = 'employee',
                            employee_id = employee,
                            center_id = center,
                            package_id = package,
                            type_of_visit_id = type_of_visit,
                            created_date = current_date,
                            created_time = curr_time,
                            user_read = 'false'
                        ).save()


                        name = appointment_create.employee.employee_name
                        recipient_name = appointment_create.patient.dependent_name
                        recipient_number = appointment_create.employee.mobile
                        recipient_email = appointment_create.employee.email
                        recipient_address = appointment_create.employee.address + ', ' + appointment_create.employee.city + ' - ' + appointment_create.employee.pincode
                        recipient_date_of_birth = appointment_create.patient.date_of_birth
                        recipient_dependent_relation = appointment_create.patient.dependent_relation.relation
                        center_name = appointment_create.center.center_name
                        center_address = appointment_create.center.address + ', ' + appointment_create.center.city + ' - ' + appointment_create.center.pincode
                        appointment_date_1 =appointment_create.appointment_date_1
                        appointment_date_2 = appointment_create.appointment_date_2
                        gender = appointment_create.patient.gender.gender
                        

                        invoice_date = formatted_date

                        package_name = appointment_create.package.package_name
                        package_service = appointment_create.package.type_of_service.type_of_service
                        visit_type = appointment_create.package.type_of_visit.type_of_visit
                        
                        package_amount = appointment_create.package.MRP
                        package_discount_price = appointment_create.package.discount_price
                        package_offer_price = appointment_create.package.offer_price
                    
                        amount_in_words = num2words(package_offer_price, lang='en').capitalize() + " only"
                        
                        center_state = appointment_create.center.state
                        appointment_id = appointment_create.id

                        if center_state == 'Maharashtra':
                            package_SGST = appointment_create.package.sgst
                            package_SGST_amount = appointment_create.package.sgst_amount
                            package_CGST = appointment_create.package.cgst
                            package_CGST_amount = appointment_create.package.cgst_amount

                            context= {
                                "name":name,
                                "recipient_name":recipient_name,
                                "recipient_number":recipient_number,
                                "recipient_email":recipient_email,
                                "recipient_address":recipient_address,
                                "recipient_date_of_birth":recipient_date_of_birth,
                                "recipient_dependent_relation":recipient_dependent_relation,
                                "appointment_date_1": appointment_date_1,
                                "appointment_date_2": appointment_date_2,
                                "gender":gender,

                                "center_name":center_name,
                                "center_address":center_address,
                                "invoice_id":invoice_id,
                                "invoice_date":invoice_date,
                                "booking_id":booking_id,

                                "package_name":package_name,
                                "package_service":package_service,
                                "visit_type":visit_type,
                                "package_amount":package_amount,
                                "package_discount_price":package_discount_price,
                                "amount_in_words":amount_in_words,
                                "package_offer_price":package_offer_price,
                                "method":method,
                                'amount':amount,

                                "flag":True,
                                "package_SGST":package_SGST,
                                "package_SGST_amount":package_SGST_amount,
                                "package_CGST":package_CGST,
                                "package_CGST_amount":package_CGST_amount,
                                "appointment_id":appointment_id
                            }    
                        else:
                            package_IGST = appointment_create.package.igst
                            package_IGST_amount = appointment_create.package.igst_amount
                            
                            context= {
                                "name":name,
                                "recipient_name":recipient_name,
                                "recipient_email":recipient_email,
                                "recipient_number":recipient_number,
                                "recipient_address":recipient_address,
                                "recipient_date_of_birth":recipient_date_of_birth,
                                "recipient_dependent_relation":recipient_dependent_relation,
                                "appointment_date_1": appointment_date_1,
                                "appointment_date_2": appointment_date_2,
                                "gender":gender,
                                
                                "center_name":center_name,
                                "center_address":center_address,
                                "invoice_id":invoice_id,
                                "invoice_date":invoice_date,
                                "booking_id":booking_id,
                                "method":method,
                                'amount':amount,
                                

                                "package_name":package_name,
                                "package_service":package_service,
                                "visit_type":visit_type,
                                "package_amount":package_amount,
                                "package_discount_price":package_discount_price,
                                "amount_in_words":amount_in_words,
                                "package_offer_price":package_offer_price,

                                "flag":False,
                                "package_IGST":package_IGST,
                                "package_IGST_amount":package_IGST_amount,
                                "appointment_id":appointment_id
                            }
                        
                        data = createPDF(context)
                        if recipient_email != None and recipient_email != 'null' and recipient_email != '':        
                            htmlgen = get_template("health_checkup.html").render(context)
                            send_mail('Acknowledgment of Your Health Checkup Request',"password",settings.EMAIL_HOST_USER,[recipient_email], fail_silently=False, html_message=htmlgen)
                
                        
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "You're appointment book successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "You're appointment book successfully.",
                            'appointment_id':appointment_id
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    res = {
                                'statuscode' : 406,
                                'status':'false',
                                'message':'Package with this dependent already in cart.'
                            }                                                        
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')

        elif flag == 'individual':
            check_individual = models.IndividualUserDetail.objects.filter(id = individual).count()
            list_data = []
            if check_individual == 1:
                vendor_id = models.PackageDetail.objects.filter(id = package).values_list('vendor', flat=True)[0]
                appointment_check = models.AppointmentDetail.objects.filter(individual_id = individual,individual_patient_id = patient,package_id = package, status= 'add_to_cart').count()
                if appointment_check == 0 or appointment_check == 1:
                    appointment_create = models.AppointmentDetail.objects.create(
                        individual_id = individual,  
                        appointment_type = 'Individual',
                        individual_patient_id = patient,
                        individual_address_id = address,
                        package_id = package,
                        center_id = center,
                        vendor_id = vendor_id,
                        type_of_visit_id = type_of_visit,
                        appointment_date_1 = appointment_date_1, 
                        appointment_date_2 = appointment_date_2,
                        home_sample_date_1 = home_sample_date_1,
                        home_sample_date_2 = home_sample_date_2,
                        status = status,
                        created_at = current_date
                    )
                    appointment_create.save()
                    appointment_id = appointment_create.id

                    if cart_flag != True:
                        package_data = models.PackageDetail.objects.get(id = package)
                        package_type = package_data.package_type
                        amount = package_data.offer_price
                        # corporate_id = models.EmployeeDetail.objects.filter(id = employee).values_list('corporate', flat=True)[0]

                        if is_payment == False:
                            amount = 0
                        ### Invoice Data
                        total_today_appointment = models.AppointmentDetail.objects.filter(created_at =current_date).count()
                        formatted_num = format(total_today_appointment, '03d')
                        all_appointment = models.AppointmentDetail.objects.all().count()
                        all_formatted_num = format(all_appointment, '05d')

                        booking_id = 'BKG-' + str(current_date_booking) + '-' +str(formatted_num)
                        
                        invoice_id = f'25-26/{formatted_num}/IN-{all_formatted_num}'

                        package_data = models.PackageDetail.objects.get(id = package)
                        package_type = package_data.package_type
                        amount = package_data.offer_price

                        transaction_create = models.Transaction.objects.create(
                            transaction_type = package_type,
                            appointment_id = appointment_create.id,
                            is_payment = is_payment,
                            booking_id = booking_id,
                            invoice_id = invoice_id,
                            individual_id=individual,
                            method = method,
                            transaction_id = transaction_id,
                            corporate_id=None,
                            employee_id=None,
                            package_id=package,
                            amount=amount,
                            individual_patient_id = patient,
                            status='Paid',
                            reason = 'Paid but Appointment/Report is pending.',
                            created_at=current_date
                        ).save()

                        notification = models.NotificationDetail.objects.create(
                            title = 'Health Checkup Request Received',
                            notification_type = 'Acknowledgment',
                            preferred_appointment_date1 = appointment_date_1,
                            preferred_appointment_date2 = appointment_date_2,
                            user_type = 'individual',
                            individual_id = individual,
                            center_id = center,
                            package_id = package,
                            type_of_visit_id = type_of_visit,
                            created_date = current_date,
                            created_time = curr_time,
                            user_read = 'false'
                        ).save()

                        
                        recipient_name = appointment_create.individual_patient.dependent_name
                        recipient_number = appointment_create.individual.mobile
                        recipient_email = appointment_create.individual.email
                        recipient_address = appointment_create.individual.address + ', ' + appointment_create.individual.city + ' - ' + appointment_create.individual.pincode

                        center_name = appointment_create.center.center_name
                        center_address = appointment_create.center.address + ', ' + appointment_create.center.city + ' - ' + appointment_create.center.pincode


                        invoice_date = formatted_date

                        package_name = appointment_create.package.package_name
                        package_service = appointment_create.package.type_of_service.type_of_service
                        
                        package_amount = appointment_create.package.MRP
                        package_discount_price = appointment_create.package.discount_price
                        package_offer_price = appointment_create.package.offer_price
                    
                        amount_in_words = num2words(package_offer_price, lang='en').capitalize() + " only"
                        
                        center_state = appointment_create.center.state
                        appointment_id = appointment_create.id


                        if center_state == 'Maharashtra':
                            package_SGST = appointment_create.package.sgst
                            package_SGST_amount = appointment_create.package.sgst_amount
                            package_CGST = appointment_create.package.cgst
                            package_CGST_amount = appointment_create.package.cgst_amount

                            context= {
                                "recipient_name":recipient_name,
                                "recipient_number":recipient_number,
                                "recipient_email":recipient_email,
                                "recipient_address":recipient_address,
                                
                                "center_name":center_name,
                                "center_address":center_address,
                                "invoice_id":invoice_id,
                                "invoice_date":invoice_date,
                                "booking_id":booking_id,
                                "method":method,

                                "package_name":package_name,
                                "package_service":package_service,
                                "package_amount":package_amount,
                                "package_discount_price":package_discount_price,
                                "amount_in_words":amount_in_words,
                                "package_offer_price":package_offer_price,

                                "flag":True,
                                "package_SGST":package_SGST,
                                "package_SGST_amount":package_SGST_amount,
                                "package_CGST":package_CGST,
                                "package_CGST_amount":package_CGST_amount,
                                "appointment_id":appointment_id
                            }    
                        else:
                            package_IGST = appointment_create.package.igst
                            package_IGST_amount = appointment_create.package.igst_amount
                            
                            context= {
                                "recipient_name":recipient_name,
                                "recipient_number":recipient_number,
                                "recipient_address":recipient_address,
                                "center_name":center_name,
                                "center_address":center_address,
                                "invoice_id":invoice_id,
                                "invoice_date":invoice_date,
                                "booking_id":booking_id,
                                "method":method,

                                "package_name":package_name,
                                "package_service":package_service,
                                "package_amount":package_amount,
                                "package_discount_price":package_discount_price,
                                "amount_in_words":amount_in_words,
                                "package_offer_price":package_offer_price,

                                "flag":False,
                                "package_IGST":package_IGST,
                                "package_IGST_amount":package_IGST_amount,
                                "appointment_id":appointment_id

                            }

                        data = createPDF(context)

                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "You're appointment book successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            
                    else:
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "You're appointment book successfully.",
                            'appointment_id':appointment_id
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    res = {
                                'statuscode' : 406,
                                'status':'false',
                                'message':'Package with this dependent already in cart.'
                            }                                                        
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Please Enter Individual."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:

            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Employee."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

# @csrf_exempt
# def createPDF(context):
#     now = datetime.now()
#     print(now, 'nownow')
#     formatted_date = now.strftime("%B %d, %Y")
#     current_date_data = now.strftime('%Y-%m-%d')
#     current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
#     curr_time = time.strftime("%H:%M:%S", time.localtime())
#     current_time = now.strftime("%Y%m%d%H%M%S")
#     current_date_booking = now.strftime("%Y%m%d")


#     date_time = str(current_date) + str(curr_time)
#     print(context, 'vadvdvkjdgvh')
#     recipient_name = context.get('recipient_name')
#     appointment_id = context.get('appointment_id')

#     invoice_template = get_template("invoice_template.html")
#     html_content = invoice_template.render(context)
#     options = {
            
#             'page-size': 'A4',
#             'no-outline': None,
#             'margin-top': '0mm',
#             'margin-right': '0mm',
#             'margin-bottom': '0mm',
#             'margin-left': '0mm',
#             'viewport-size': '1280x1024'
#         }
#     pdf = pdfkit.from_string(html_content, False, options=options)
#     pdf_name = f'invoice_{recipient_name +"_"+ date_time}.pdf'
#     pdf_file = ContentFile(pdf, name=pdf_name)
#     transaction = models.Transaction.objects.get(appointment = appointment_id)
#     transaction.invoice.save(pdf_file.name, pdf_file) 
#     transaction.save()

#     return None





@csrf_exempt
def appointment_booking_reschedule(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        appointment = python_data.get('appointment')
        status = python_data.get('status')

        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        curr_time = time.strftime("%H:%M:%S", time.localtime())
        check_appointment = models.AppointmentDetail.objects.filter(id = appointment).count()
        if check_appointment == 1:
            if status == 'Confirmed':
                appointment = models.AppointmentDetail.objects.get(id = appointment)
                appointment.remark = python_data.get('remark', appointment.remark)
                appointment.confirm_appointment_date = python_data.get('confirm_appointment_date', appointment.confirm_appointment_date)
                appointment.confirm_home_sample_date = python_data.get('confirm_home_sample_date', appointment.confirm_home_sample_date)
                appointment.status = 'Confirmed'
                appointment.save()
                
                type_of_visit = models.PackageDetail.objects.filter(id = appointment.package.id).values_list('type_of_visit', flat=True)[0]
                
                if appointment.appointment_type == "Employee":
                    individual = None
                    employee = appointment.employee.id
                    patient_name = appointment.patient.dependent_name
                    recipient_email = appointment.employee.email
                
                if appointment.appointment_type == "Individual":
                    employee = None
                    individual = appointment.individual.id
                    patient_name = appointment.patient.dependent_name
                    recipient_email = appointment.individual.email



                notification = models.NotificationDetail.objects.create(
                    title = 'Health Check-up Appointment Confirmed',
                    notification_type = 'Confirmation Appointment',
                    preferred_appointment_date1 = appointment.confirm_appointment_date,
                    preferred_appointment_date2 = appointment.confirm_home_sample_date,
                    user_type = (appointment.appointment_type).lower(),
                    individual_id = individual,
                    employee_id = employee,
                    center_id = appointment.center.id,
                    package_id = appointment.package.id,
                    type_of_visit_id = type_of_visit,
                    created_date = current_date,
                    created_time = curr_time,
                    user_read = 'false'
                )
                notification.save()

                context ={
                    "patient_name":patient_name,
                    "appointment_date":appointment.confirm_appointment_date,
                    "center_name":appointment.center.center_name,
                    "center_address":appointment.center.address,
                    "package_name":appointment.package.package_name

                }

                if recipient_email != None and recipient_email != 'null' and recipient_email != '':        
                    htmlgen = get_template("appointment_confirmation.html").render(context)
                    send_mail('Your Upcoming Health Check-up – Appointment Confirmation',"password",'setting.EMAIL_HOST_USER',[recipient_email], fail_silently=False, html_message=htmlgen)
            

                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Your appointment Booked successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')
            
            elif status == 'Rescheduled':
                appointment = models.AppointmentDetail.objects.get(id = appointment)
                old_appointment_date = appointment.confirm_appointment_date or appointment.appointment_date_1
                old_home_sample_date = appointment.confirm_home_sample_date or appointment.home_sample_date_1
                new_appointment_date = python_data.get('confirm_appointment_date', appointment.confirm_appointment_date)
                new_home_sample_date = python_data.get('confirm_home_sample_date', appointment.confirm_home_sample_date)
                rescheduled_by = python_data.get('rescheduled_by', appointment.appointment_type)
                reason = python_data.get('reason', appointment.reason)
                remark = python_data.get('remark', appointment.remark)

                reschedule_record = models.RescheduleAppointment.objects.create(
                    appointment=appointment,
                    rescheduled_by=rescheduled_by,
                    old_appointment_date=old_appointment_date,
                    new_appointment_date=new_appointment_date,
                    old_home_sample_date=old_home_sample_date,
                    new_home_sample_date=new_home_sample_date,
                    reason=reason,
                    remark=remark,
                    status='Rescheduled',
                    created_at=current_date
                )

                appointment.remark = remark
                appointment.reason = reason
                appointment.confirm_appointment_date = new_appointment_date
                appointment.confirm_home_sample_date = new_home_sample_date
                appointment.status = 'Rescheduled'
                appointment.save()

                reschedule_serializer = RescheduleAppointmentSerializer(reschedule_record)
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Your appointment Rescheduled successfully.",
                    'data': reschedule_serializer.data
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter valid Status."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')   

        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid appointment."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def reschedule_appointment_list(request):
    if request.method in ['POST', 'GET']:
        if request.method == 'POST':
            python_data = JSONParser().parse(io.BytesIO(request.body))
            appointment_id = python_data.get('appointment_id') or python_data.get('appointment')
        else:
            appointment_id = request.GET.get('appointment_id') or request.GET.get('appointment')

        if appointment_id:
            records = models.RescheduleAppointment.objects.filter(appointment_id=appointment_id).order_by('-id')
        else:
            records = models.RescheduleAppointment.objects.all().order_by('-id')

        serializer = RescheduleAppointmentSerializer(records, many=True)
        res = {
            'statuscode': 200,
            'status': 'true',
            'data': serializer.data
        }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')






@csrf_exempt
def appointment_cancel_done(request):
    if request.method == 'POST':
        python_data={}
        for i,j in request.FILES.items():
            python_data.update({i:j})
        
        for i,j in request.POST.items():
            python_data.update({i:j})

        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        curr_time = time.strftime("%H:%M:%S", time.localtime())

        appointment = python_data.get('appointment')
        status = python_data.get('status')
        check_appointment = models.AppointmentDetail.objects.filter(id = appointment).count()
        if check_appointment == 1:
            if status == 'Cancel':
                appointment = models.AppointmentDetail.objects.get(id = appointment)
                appointment.reason = python_data.get('reason', appointment.reason)
                appointment.status = 'Cancel'
                appointment.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Your appointment Cancel successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')
            
            elif status == 'Reports Uploaded':
                appointment = models.AppointmentDetail.objects.get(id = appointment)
                
                if type(python_data.get('report', appointment.report)) != str:         
                    appointment.report = python_data.get('report', appointment.report)
                    appointment.report_date = current_date
                    # appointment.report_date = python_data.get('report_date', appointment.report_date)

                appointment.status = 'Reports Uploaded'
                appointment.save()
                transaction = models.Transaction.objects.get(appointment = appointment)
                transaction.reason = 'Appointment done and Report Uploaded.'
                transaction.status = 'Complete'
                transaction.save()
                
                appointment_type = appointment.appointment_type
                if (appointment_type).lower() == 'employee':
                    recipient_name = appointment.patient.dependent_name
                    employee = appointment.employee.id
                    individual = None
                    recipient_email =appointment.employee.email
                else:
                    recipient_name = appointment.individual_patient.dependent_name
                    individual = appointment.individual.id
                    employee = None
                    recipient_email =appointment.individual.email

                notification = models.NotificationDetail.objects.create(
                    title = 'Your Health Check-Up Report is Ready!',
                    notification_type = 'Report Ready',
                    user_type = appointment_type,
                    employee_id = employee,
                    individual_id = individual,
                    recipient_name = recipient_name,
                    created_date = current_date,
                    created_time = curr_time,
                    user_read = 'false'
                ).save()

                context={
                    "recipient_name":recipient_name
                }
                if recipient_email != None and recipient_email != 'null' and recipient_email != '':        
                    htmlgen = get_template("report_upload.html").render(context)
                    send_mail('Your Health Check-Up Report – We Value Your Feedback 💙',"password",'setting.EMAIL_HOST_USER',[recipient_email], fail_silently=False, html_message=htmlgen)
                    
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Your appointment Done successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')
            
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter valid Status."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')   

        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid appointment."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def appointment_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        appointment = python_data.get('id')
        check_appointment = models.AppointmentDetail.objects.filter(id = appointment).count()
        if check_appointment == 1:
            
            appointment_details = models.AppointmentDetail.objects.get(id = appointment)
            appointment_details.status = 'Pending'
            appointment_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "appointment Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid appointment ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 






@csrf_exempt
def all_appointment_list(request):
    if request.method == 'POST':
        get_data={}
        for i,j in request.FILES.items():
            get_data.update({i:j})
        
        for i,j in request.POST.items():
            get_data.update({i:j})

        base64_string = get_data.get('data')
        base64_bytes = base64_string.encode("ascii")
        string_bytes = base64.b64decode(base64_bytes)
        python_data = string_bytes.decode("ascii")
        python_data = json.loads(python_data)
        
        employee_total_records = 0
        individual_totals_records = 0

        page_number = int(python_data.get('page_number',1))
        row_size = int(python_data.get('row_size',10))
        last_row = row_size * page_number
        first_row = last_row - row_size

        id = python_data.get('id')
        # id = request.POST['id']
        check_staff = models.StaffDetail.objects.filter(id = id).count()
        if check_staff == 1:
            staff_id = models.StaffDetail.objects.get(id = id)
            get_type_access = staff_id.type_of_access.type_of_access
            if get_type_access == 'Super Admin' or get_type_access == 'Admin': 

                corporate_name = python_data.get('corporate_name', None)
                employee_name = python_data.get('employee_name', None)
                individual_name = python_data.get('individual_name', None)
                patient_name = python_data.get('patient_name', None)
                address_short = python_data.get('address_short', None)
                package_name = python_data.get('package_name', None)
                package_price = python_data.get('package_price', None)
                type_of_service = python_data.get('type_of_service', None)
                type_of_visit = python_data.get('type_of_visit', None)
                center_name = python_data.get('center_name', None)
                vendor_name = python_data.get('vendor_name', None)
                created_at = python_data.get('created_at', None)
                appointment_date_1 = python_data.get('appointment_date_1', None)
                appointment_date_2 = python_data.get('appointment_date_2', None)
                home_sample_date_1 = python_data.get('home_sample_date_1', None)
                home_sample_date_2 = python_data.get('home_sample_date_2', None)
                confirm_appointment_date = python_data.get('confirm_appointment_date', None)
                confirm_home_sample_date = python_data.get('confirm_home_sample_date', None)
                report_date = python_data.get('report_date', None)
                status = python_data.get('status', None)


                filter_condition = {}

                # Corporate & Individual
                if corporate_name not in [None, '', 'null']:
                    filter_condition['corporate_name__icontains'] = corporate_name

                if employee_name not in [None, '', 'null']:
                    filter_condition['employee__employee_name__icontains'] = employee_name

                if individual_name not in [None, '', 'null']:
                    filter_condition['individual__name__icontains'] = individual_name

                # Patient & Address
                if patient_name not in [None, '', 'null']:
                    filter_condition['individual_patient__dependent_name__icontains'] = patient_name

                if address_short not in [None, '', 'null']:
                    filter_condition['individual__address__icontains'] = address_short

                # Package details
                if package_name not in [None, '', 'null']:
                    filter_condition['package__package_name__icontains'] = package_name

                if package_price not in [None, '', 'null']:
                    filter_condition['package__offer_price__icontains'] = package_price

                # Service & Visit details
                if type_of_service not in [None, '', 'null']:
                    filter_condition['package__type_of_service__type_of_service__icontains'] = type_of_service

                if type_of_visit not in [None, '', 'null']:
                    filter_condition['type_of_visit__type_of_visit__icontains'] = type_of_visit

                # Center & Vendor
                if center_name not in [None, '', 'null']:
                    filter_condition['center__center_name__icontains'] = center_name

                if vendor_name not in [None, '', 'null']:
                    filter_condition['vendor__vendor_name__icontains'] = vendor_name

                # Dates
                if created_at not in [None, '', 'null']:
                    filter_condition['created_at__icontains'] = created_at

                if appointment_date_1 not in [None, '', 'null']:
                    filter_condition['appointment_date_1__icontains'] = appointment_date_1

                if appointment_date_2 not in [None, '', 'null']:
                    filter_condition['appointment_date_2__icontains'] = appointment_date_2

                if home_sample_date_1 not in [None, '', 'null']:
                    filter_condition['home_sample_date_1__icontains'] = home_sample_date_1

                if home_sample_date_2 not in [None, '', 'null']:
                    filter_condition['home_sample_date_2__icontains'] = home_sample_date_2

                if confirm_appointment_date not in [None, '', 'null']:
                    filter_condition['confirm_appointment_date__icontains'] = confirm_appointment_date

                if confirm_home_sample_date not in [None, '', 'null']:
                    filter_condition['confirm_home_sample_date__icontains'] = confirm_home_sample_date

                if report_date not in [None, '', 'null']:
                    filter_condition['report_date__icontains'] = report_date
                
                if status not in [None, '', 'null']:
                    if status != 'All':
                        filter_condition['status__icontains'] = status


                all_appointment = models.AppointmentDetail.objects.filter(**filter_condition).exclude(status='add_to_cart').order_by('-id')
                serialiser = AppointmentDetailSerializer(all_appointment, many=True)

                employee_total_records = models.AppointmentDetail.objects.filter(**filter_condition, appointment_type = 'Employee').exclude(status='add_to_cart').count()
                all_appointment_employee = models.AppointmentDetail.objects.filter(**filter_condition, appointment_type = 'Employee').exclude(status='add_to_cart').order_by('-id')[first_row:last_row]
                employee_serialiser = AppointmentDetailSerializer(all_appointment_employee, many=True)
                list_employee_data = employee_serialiser.data
                
                individual_totals_records = models.AppointmentDetail.objects.filter(**filter_condition, appointment_type = 'Individual').exclude(status='add_to_cart').count()
                all_appointment_individual = models.AppointmentDetail.objects.filter(**filter_condition, appointment_type = 'Individual').exclude(status='add_to_cart').order_by('-id')[first_row:last_row]
                individual_serialiser = AppointmentDetailSerializer(all_appointment_individual, many=True)
                list_individual_data = individual_serialiser.data
            
            else:
                list_employee_data = []

                staff_assign_to = models.StaffDetail.objects.filter(id = id).values_list('assign_to', flat=True)[0]
                if staff_assign_to == 'Corporate':
                    corporate_name = python_data.get('corporate_name',None)
                    employee_name = python_data.get('employee_name',None)
                    patient_name = python_data.get('patient_name',None)
                    address_short = python_data.get('address_short',None)
                    package_name = python_data.get('package_name',None)
                    package_price = python_data.get('package_price',None)
                    type_of_service = python_data.get('type_of_service',None)
                    type_of_visit = python_data.get('type_of_visit',None)
                    center_name = python_data.get('center_name',None)
                    vendor_name = python_data.get('vendor_name',None)
                    created_at = python_data.get('created_at',None)
                    appointment_date_1 = python_data.get('appointment_date_1',None)
                    appointment_date_2 = python_data.get('appointment_date_2',None)
                    home_sample_date_1 = python_data.get('home_sample_date_1',None)
                    home_sample_date_2 = python_data.get('home_sample_date_2',None)
                    confirm_appointment_date = python_data.get('confirm_appointment_date',None)
                    confirm_home_sample_date = python_data.get('confirm_home_sample_date',None)
                    report_date = python_data.get('report_date',None)

                    filter_condition = {}

                    if corporate_name not in [None,'','null']:
                        filter_condition['corporate_name__icontains'] = corporate_name
                    if employee_name not in [None,'','null']:
                        filter_condition['employee__employee_name__icontains'] = employee_name
                    if patient_name not in [None,'','null']:
                        filter_condition['patient__dependent_name__icontains'] = patient_name
                    if address_short not in [None,'','null']:
                        filter_condition['address_short__icontains'] = address_short
                    if package_name not in [None,'','null']:
                        filter_condition['package__package_name__icontains'] = package_name
                    if package_price not in [None,'','null']:
                        filter_condition['package__package_price__icontains'] = package_price
                    if type_of_service not in [None,'','null']:
                        filter_condition['type_of_service__icontains'] = type_of_service
                    if type_of_visit not in [None,'','null']:
                        filter_condition['type_of_visit__type_of_visit__icontains'] = type_of_visit
                    if center_name not in [None,'','null']:
                        filter_condition['center__center_name__icontains'] = center_name
                    if vendor_name not in [None,'','null']:
                        filter_condition['vendor__vendor_name__icontains'] = vendor_name
                    if created_at not in [None,'','null']:
                        filter_condition['created_at__icontains'] = created_at
                    if appointment_date_1 not in [None,'','null']:
                        filter_condition['appointment_date_1__icontains'] = appointment_date_1
                    if appointment_date_2 not in [None,'','null']:
                        filter_condition['appointment_date_2__icontains'] = appointment_date_2
                    if home_sample_date_1 not in [None,'','null']:
                        filter_condition['home_sample_date_1__icontains'] = home_sample_date_1
                    if home_sample_date_2 not in [None,'','null']:
                        filter_condition['home_sample_date_2__icontains'] = home_sample_date_2
                    if confirm_appointment_date not in [None,'','null']:
                        filter_condition['confirm_appointment_date__icontains'] = confirm_appointment_date
                    if confirm_home_sample_date not in [None,'','null']:
                        filter_condition['confirm_home_sample_date__icontains'] = confirm_home_sample_date
                    if report_date not in [None,'','null']:
                        filter_condition['report_date__icontains'] = report_date


                    
                    all_corporate = models.CorporateDetail.objects.filter(Q(level1 =staff_id) | Q(level2 =staff_id )).distinct()
                    serialiser = CorporateSerializer(all_corporate, many=True)
                    for corporate in all_corporate:
                        get_all_employee = models.EmployeeDetail.objects.filter(corporate = corporate.id)
                        list_individual_data = []
                        for employee in get_all_employee:
                            employee_total_records = models.AppointmentDetail.objects.filter(**filter_condition,employee= employee, appointment_type = 'Employee').exclude(status='add_to_cart').count()
                            all_appointment_employee = models.AppointmentDetail.objects.filter(**filter_condition,employee= employee, appointment_type = 'Employee').exclude(status='add_to_cart').order_by('-id')[first_row:last_row]
                            employee_serialiser = AppointmentDetailSerializer(all_appointment_employee, many=True)
                            list_employee_data.append(employee_serialiser.data)

                    list_employee_data = sum(list_employee_data, [])
                
                elif staff_assign_to == 'Individual':
                    individual_name = python_data.get('individual_name',None)
                    patient_name = python_data.get('patient_name',None)
                    address_short = python_data.get('address_short',None)
                    package_name = python_data.get('package_name',None)
                    package_price = python_data.get('package_price',None)
                    type_of_service = python_data.get('type_of_service',None)
                    type_of_visit = python_data.get('type_of_visit',None)
                    center_name = python_data.get('center_name',None)
                    vendor_name = python_data.get('vendor_name',None)
                    created_at = python_data.get('created_at',None)
                    appointment_date_1 = python_data.get('appointment_date_1',None)
                    appointment_date_2 = python_data.get('appointment_date_2',None)
                    home_sample_date_1 = python_data.get('home_sample_date_1',None)
                    home_sample_date_2 = python_data.get('home_sample_date_2',None)
                    confirm_appointment_date = python_data.get('confirm_appointment_date',None)
                    confirm_home_sample_date = python_data.get('confirm_home_sample_date',None)
                    report_date = python_data.get('report_date',None)

                    filter_condition = {}

                    if individual_name not in [None, '', 'null']:
                        filter_condition['individual__individual_name__icontains'] = individual_name

                    if patient_name not in [None, '', 'null']:
                        filter_condition['patient__patient_name__icontains'] = patient_name

                    if address_short not in [None, '', 'null']:
                        filter_condition['address_short__icontains'] = address_short

                    if package_name not in [None, '', 'null']:
                        filter_condition['package__package_name__icontains'] = package_name

                    if package_price not in [None, '', 'null']:
                        filter_condition['package__package_price__icontains'] = package_price

                    if type_of_service not in [None, '', 'null']:
                        filter_condition['type_of_service__icontains'] = type_of_service

                    if type_of_visit not in [None, '', 'null']:
                        filter_condition['type_of_visit__type_of_visit__icontains'] = type_of_visit

                    if center_name not in [None, '', 'null']:
                        filter_condition['center__center_name__icontains'] = center_name

                    if vendor_name not in [None, '', 'null']:
                        filter_condition['vendor__vendor_name__icontains'] = vendor_name

                    if created_at not in [None, '', 'null']:
                        filter_condition['created_at__icontains'] = created_at

                    if appointment_date_1 not in [None, '', 'null']:
                        filter_condition['appointment_date_1__icontains'] = appointment_date_1

                    if appointment_date_2 not in [None, '', 'null']:
                        filter_condition['appointment_date_2__icontains'] = appointment_date_2

                    if home_sample_date_1 not in [None, '', 'null']:
                        filter_condition['home_sample_date_1__icontains'] = home_sample_date_1

                    if home_sample_date_2 not in [None, '', 'null']:
                        filter_condition['home_sample_date_2__icontains'] = home_sample_date_2

                    if confirm_appointment_date not in [None, '', 'null']:
                        filter_condition['confirm_appointment_date__icontains'] = confirm_appointment_date

                    if confirm_home_sample_date not in [None, '', 'null']:
                        filter_condition['confirm_home_sample_date__icontains'] = confirm_home_sample_date

                    if report_date not in [None, '', 'null']:
                        filter_condition['report_date__icontains'] = report_date


                    list_employee_data = []
                    list_individual_data = []

                    individual_totals_records = models.AppointmentDetail.objects.filter(**filter_condition, appointment_type = 'Individual').exclude(status='add_to_cart').count()
                    all_appointment_individual = models.AppointmentDetail.objects.filter(**filter_condition, appointment_type = 'Individual').exclude(status='add_to_cart').order_by('-id')[first_row:last_row]
                    individual_serialiser = AppointmentDetailSerializer(all_appointment_individual, many=True)
                    list_individual_data.append(individual_serialiser.data)

        res = {
            'statuscode' : 200,
            'status':'true',
            # 'data' : serialiser.data,
            'employee_data':list_employee_data,
            'employee_total_records':employee_total_records,
            'individual_data':list_individual_data,
            'individual_totals_records':individual_totals_records
        }
        
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 



# @csrf_exempt
# def all_appointment_list_corporate(request):
#     if request.method == 'POST':
#         get_data={}
#         for i,j in request.FILES.items():
#             get_data.update({i:j})
        
#         for i,j in request.POST.items():
#             get_data.update({i:j})

#         base64_string = get_data.get('data')
#         base64_bytes = base64_string.encode("ascii")
#         string_bytes = base64.b64decode(base64_bytes)
#         python_data = string_bytes.decode("ascii")
#         python_data = json.loads(python_data)

#         print("python_data--=-=-->",python_data)
        
#         id = python_data.get('id',None)

#         corporate_name = python_data.get('corporate_name',None)
#         employee_name = python_data.get('employee_name',None)
#         patient_name = python_data.get('patient_name',None)
#         address_short = python_data.get('address_short',None)
#         package_name = python_data.get('package_name',None)
#         package_price = python_data.get('package_price',None)
#         type_of_service = python_data.get('type_of_service',None)
#         type_of_visit = python_data.get('type_of_visit',None)
#         center_name = python_data.get('center_name',None)
#         vendor_name = python_data.get('vendor_name',None)
#         created_at = python_data.get('created_at',None)
#         appointment_date_1 = python_data.get('appointment_date_1',None)
#         appointment_date_2 = python_data.get('appointment_date_2',None)
#         home_sample_date_1 = python_data.get('home_sample_date_1',None)
#         home_sample_date_2 = python_data.get('home_sample_date_2',None)
#         confirm_appointment_date = python_data.get('confirm_appointment_date',None)
#         confirm_home_sample_date = python_data.get('confirm_home_sample_date',None)
#         report_date = python_data.get('report_date',None)






@csrf_exempt
def appointment_list_for_vendor(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        vendor = python_data.get('vendor')
        check_vendor = models.VendorDetail.objects.filter(id = vendor).count()
        if check_vendor == 1:
            all_appointment = models.AppointmentDetail.objects.filter(vendor = vendor).exclude(status='add_to_cart').order_by('-id')
            serialiser = AppointmentDetailSerializer(all_appointment, many=True)

            done_appointment_count = models.AppointmentDetail.objects.filter(vendor = vendor, status = 'Reports Uploaded').count()
            cancel_appointment_count = models.AppointmentDetail.objects.filter(vendor = vendor, status = 'Cancel').count()
            booking_appointment_count = models.AppointmentDetail.objects.filter(vendor = vendor, status = 'Confirmed').count()
            reschedule_appointment_count = models.AppointmentDetail.objects.filter(vendor = vendor, status = 'Rescheduled').count()

            res = {
                'statuscode' : 200,
                'status':'true',
                'data' : serialiser.data,
                'done_appointment_count':done_appointment_count,
                'cancel_appointment_count':cancel_appointment_count,
                'booking_appointment_count':booking_appointment_count,
                'reschedule_appointment_count':reschedule_appointment_count
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid Vendor ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 





@csrf_exempt
def employee_appointment_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        employee = python_data.get('employee')
        all_appointment = models.AppointmentDetail.objects.filter(employee = employee).exclude(status='add_to_cart').order_by('-id')
        
        serialiser = AppointmentDetailSerializer(all_appointment, many=True)
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def individual_appointment_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        individual = python_data.get('individual')
        all_appointment = models.AppointmentDetail.objects.filter(individual = individual).exclude(status='add_to_cart').order_by('-id')
        
        serialiser = AppointmentDetailSerializer(all_appointment, many=True)
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def tomorrow_check(request):
    if request.method == 'POST':
        
        now = datetime.now()
        formatted_date = now.strftime("%B %d, %Y")
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        curr_time = time.strftime("%H:%M:%S", time.localtime())
        current_time = now.strftime("%Y%m%d%H%M%S")

        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        curr_time = time.strftime("%H:%M:%S", time.localtime())

        presentday = datetime.now()
        tomorrow = presentday + timedelta(1)
        tomorrow = tomorrow.strftime('%Y-%m-%d')

        check_already_send = models.NotificationDetail.objects.filter(notification_type = 'Gentle Reminder',appointment_date = tomorrow).count()
        if check_already_send == 0:
            get_center_id = models.TypeOfVisit.objects.filter(type_of_visit='At Center').values_list('id', flat=True)[0]
            get_hybrid_id = models.TypeOfVisit.objects.filter(type_of_visit='Hybrid').values_list('id', flat=True)[0]
            list_appointment = models.AppointmentDetail.objects.filter(Q(type_of_visit = get_center_id) | Q(type_of_visit = get_hybrid_id), confirm_appointment_date =tomorrow)
            for appointment in list_appointment:
                get_data = models.AppointmentDetail.objects.get(id = appointment.id)
                center_address = get_data.center.center_name + ', ' + get_data.center.address + ', ' + get_data.center.city + '-' + get_data.center.pincode
                package = get_data.package.id
                center = get_data.center.id
                
                appointment_type = get_data.appointment_type
                if (appointment_type).lower() == 'employee':
                    recipient_name = appointment.patient.dependent_name
                    employee = appointment.employee.id
                    individual = None
                else:
                    recipient_name = appointment.individual_patient.dependent_name
                    individual = appointment.individual.id
                    employee = None

                notification = models.NotificationDetail.objects.create(
                    title = 'Gentle Reminder: Your Health Check-Up is Tomorrow',
                    notification_type = 'Gentle Reminder',
                    # appointment_date = tomorrow,
                    user_type = appointment_type,
                    employee_id = employee,
                    individual_id = individual,
                    center_id = center,
                    package_id = package,
                    location = center_address,
                    recipient_name = recipient_name,
                    appointment_date= tomorrow,
                    created_date = current_date,
                    created_time = curr_time,
                    user_read = 'false'
                ).save()
        else:
            pass

        res = {
            'statuscode' : 200,
            'status':'true',
            
        }                                                        
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json')



@csrf_exempt
def appointment_date_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_appointment = models.AppointmentDetail.objects.filter(id = id).count()
        if check_appointment == 1:
            appointment = models.AppointmentDetail.objects.get(id = id)
            appointment.appointment_date_1 = python_data.get('appointment_date_1', appointment.appointment_date_1)
            appointment.appointment_date_2 = python_data.get('appointment_date_2', appointment.appointment_date_2)
            appointment.home_sample_date_1 = python_data.get('home_sample_date_1', appointment.home_sample_date_1)
            appointment.home_sample_date_2 = python_data.get('home_sample_date_2', appointment.home_sample_date_2)
            appointment.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message':"Date Selected Successfully."
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'False',
                'message':"Something went wrong."
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')



@csrf_exempt
def appointment_export(request):
    if request.method == "POST":
        package_list = models.AppointmentDetail.objects.all().order_by('id')
        serialiser = AppointmentExportSerialiser(package_list, many=True).data
        
        headers = ['appointment_type','package','center','vendor','type_of_visit','employee','patient',
        'individual','individual_patient','report','appointment_date_1','appointment_date_2',
        'home_sample_date_1','home_sample_date_2','confirm_appointment_date','confirm_home_sample_date',
        'reason','remark','report_date','status','created_at']

        wb = op.Workbook()
        ws = wb.active
        ws.title = "Users"
        ws.append(headers) 
        
        field_map = {
            
            'appointment_type':'appointment_type', 
            'package':'package', 
            'center':'center', 
            'vendor':'vendor', 
            'type_of_visit':'type_of_visit', 
            'employee':'employee', 
            'patient':'patient', 
            'individual':'individual', 
            'individual_patient':'individual_patient', 
            'report':'report', 
            'appointment_date_1':'appointment_date_1', 
            'appointment_date_2':'appointment_date_2', 
            'home_sample_date_1':'home_sample_date_1', 
            'home_sample_date_2':'home_sample_date_2', 
            'confirm_appointment_date':'confirm_appointment_date', 
            'confirm_home_sample_date':'confirm_home_sample_date', 
            'reason':'reason', 
            'remark':'remark', 
            'report_date':'report_date', 
            'status':'status', 
            'created_at':'created_at'    

        }
        
        
        for row in serialiser:
            ws.append([row.get(field_map[h], "") for h in headers])
        
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="appointment_list.xlsx"'
        wb.save(response)

        return response


