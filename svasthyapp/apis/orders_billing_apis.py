from svasthyapp.apis.base import *
from svasthyapp.models import orders_billing_models

@csrf_exempt
def all_payment_tags_list(request):
    if request.method == 'POST':
        all_payment_tags = models.PaymentTags.objects.all().order_by('-id')
        serialiser = PaymentTagsSerializer(all_payment_tags, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 




def createPDF(context):
    def generate_pdf():
        now = datetime.now()
        formatted_date = now.strftime("%B %d, %Y")
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        curr_time = now.strftime("%H:%M:%S")
        date_time = str(current_date) + str(curr_time)

        recipient_name = context.get('recipient_name')
        appointment_id = context.get('appointment_id')

        invoice_template = get_template("invoice_template.html")
        html_content = invoice_template.render(context)

        options = {
            'page-size': 'A4',
            'no-outline': None,
            'margin-top': '0mm',
            'margin-right': '0mm',
            'margin-bottom': '0mm',
            'margin-left': '0mm',
            'viewport-size': '1280x1024'
        }
        
        path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        
        pdf = pdfkit.from_string(html_content, False, options=options, configuration=config)
        # pdf = pdfkit.from_string(html_content, False, options=options)
        
        pdf_name = f'invoice_{recipient_name +"_"+ date_time}.pdf'
        pdf_file = ContentFile(pdf, name=pdf_name)

        transaction = models.Transaction.objects.get(appointment=appointment_id)
        transaction.invoice.save(pdf_file.name, pdf_file)
        transaction.save()

    pdf_thread = threading.Thread(target=generate_pdf)
    pdf_thread.start()




@csrf_exempt
def create_order_apiview(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        amount = python_data.get('amount')

        
        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            amount = float(python_data.get("amount", 0)) * 100  # Razorpay requires amount in paise
            currency = "INR"
            order_data = {
                "amount": amount,
                "currency": currency,
                "payment_capture": 1,  # Auto capture payment
            }
            order = client.order.create(order_data)
            
            res = {
                'statuscode' : 200,
                'status':'true',
                "order_id": order["id"],
                "amount":amount / 100,
                'message':'Payment successful!'
                }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        
        except Exception as e:

            # return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            res = {
                'statuscode' : 406,
                'status':'true',
                "error": str(e),
                'message':'Payment successful!'
                } 
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')



@csrf_exempt
def verify_payment_apiview(request):
    if request.method == 'POST':
        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        python_data = JSONParser().parse(io.BytesIO(request.body))
        
    
        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_payment_id = python_data.get("razorpay_payment_id")
            razorpay_order_id = python_data.get("razorpay_order_id")
            razorpay_signature = python_data.get("razorpay_signature")
            # package = python_data.get("package")
            amount = python_data.get("amount")
            user = python_data.get("user")

            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }

            # Verify the payment signature
            client.utility.verify_payment_signature(params_dict)
            
        
            fetch_data = client.payment.fetch(razorpay_payment_id)
            method = fetch_data.get('method')
            transaction_id = fetch_data.get('id')
            res = {
                'statuscode' : 200,
                'status':'true',
                'message':'Payment successful!',
                'method': method,
                'transaction_id': transaction_id,
                }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')

        except razorpay.errors.SignatureVerificationError:
            
            res = {
                'statuscode' : 400,
                'status':'false',
                'message':'Payment verification failed!'
                }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')




@csrf_exempt
def all_transaction_list(request):
    if request.method == 'POST':
        
        all_transaction = models.Transaction.objects.all().order_by('-id')
        serialiser = TransactionSerializer(all_transaction, many=True)
        res = {
            'statuscode' : 200,
            'status':'true',
            'data':serialiser.data
        }                                                        
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json')
    


@csrf_exempt
def user_transaction_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        flag = python_data.get('flag')
        user = python_data.get('user')
        if flag == 'individual':
            all_transaction = models.Transaction.objects.filter(individual = user).order_by('-id')
            serialiser = TransactionSerializer(all_transaction, many=True)
            res = {
                'statuscode' : 200,
                'status':'true',
                'data':serialiser.data
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'employee':
            all_transaction = models.Transaction.objects.filter(employee = user).order_by('-id')
            serialiser = TransactionSerializer(all_transaction, many=True)
            res = {
                'statuscode' : 200,
                'status':'true',
                'data':serialiser.data
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 460,
                'status':'false',
                'message':'Something went wrong.'
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')

    


def invoice_template(request):
    return render(request, 'invoice_template.html')





@csrf_exempt
def add_to_cart_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        user_type = python_data.get('user_type')
        appointment = python_data.get('appointment')
        if user_type == 'employee':
            employee = python_data.get('employee')
            patient = python_data.get('patient')
            package = python_data.get('package')
            check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
            if check_employee == 1:
                check_dependent = models.EmployeeDependent.objects.filter(employee = employee, id = patient).count()
                if check_dependent == 1:
                    check_package = models.PackageDetail.objects.filter(id = package).count()
                    if check_package == 1:
                        get_amount = models.PackageDetail.objects.filter(id = package).values_list('offer_price', flat=True)[0]
                        check_add_to_cart = models.AddToCart.objects.filter(employee_id = employee,patient_id = patient,package_id = package).count()
                        if check_add_to_cart == 0:
                            add_to_cart = models.AddToCart.objects.create(
                                user_type = python_data.get('user_type'),
                                appointment_id = appointment,
                                employee_id = employee,
                                patient_id = patient,
                                package_id = package,
                                amount = get_amount,
                                individual_id = None,
                                individual_patient_id = None,
                                created_at = current_date
                            )
                            add_to_cart.save()
                            res = {
                                'statuscode' : 200,
                                'status':'true',
                                'message':'Your Package Added to Cart.'
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
                            'message':'Enter valid Package.'
                        }                                                        
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message':'Enter valid Dependent.'
                    }                                                        
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')         
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message':'Enter valid Employee.'
                }                                                        
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')    

        elif user_type == 'individual':
            individual = python_data.get('individual')
            individual_patient = python_data.get('patient')
            package = python_data.get('package')
            check_individual = models.IndividualUserDetail.objects.filter(id = individual).count()
            if check_individual == 1:
                check_dependent = models.IndividualDependent.objects.filter(individual = individual, id = individual_patient).count()
                if check_dependent == 1:
                    check_package = models.PackageDetail.objects.filter(id = package).count()
                    if check_package == 1:
                        get_amount = models.PackageDetail.objects.filter(id = package).values_list('offer_price', flat=True)[0]
                        check_add_to_cart = models.AddToCart.objects.filter(individual_id = individual,individual_patient_id = individual_patient,package_id = package).count()
                        if check_add_to_cart == 0:

                            add_to_cart = models.AddToCart.objects.create(
                                user_type = python_data.get('user_type'),
                                appointment_id = appointment,
                                employee_id = None,
                                patient_id = None,
                                package_id = package,
                                amount = get_amount,
                                individual_id = individual,
                                individual_patient_id = individual_patient,
                                created_at = current_date
                            )
                            add_to_cart.save()
                            res = {
                                'statuscode' : 200,
                                'status':'true',
                                'message':'Your Package Added to Cart.'
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
                            'message':'Enter valid Package.'
                        }                                                        
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message':'Enter valid Dependent.'
                    }                                                        
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')         
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message':'Enter valid Individual.'
                }                                                        
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message':'Enter valid User Type.'
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')




@csrf_exempt
def add_to_cart_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        user_type = python_data.get('user_type')
        id = python_data.get('id')

        total_amount = 0
        platform_charge = 0

        if user_type == 'employee':
            get_all_data = models.AddToCart.objects.filter(employee = id).order_by('-id')
            list_data = []
            for data in get_all_data:
                get_data = models.AddToCart.objects.get(id = data.id)
                
                package = data.package.id
                employee = data.employee.id
                patient = data.patient.id
                
                get_package_payment_tags = models.PackageDetail.objects.filter(id = package).values_list('tags', flat=True)[0]
                package_payment_tags = models.PaymentTags.objects.filter(id = get_package_payment_tags).values_list('payment_tags', flat=True)[0]
                
                if package_payment_tags == 'Corporate pay':
                    check_appointment = models.AppointmentDetail.objects.filter(package =package, employee =employee, patient= patient).exclude(status='add_to_cart').count()
                    if check_appointment != 0:
                        amount = data.amount
                    
                    elif check_appointment == 0:
                        amount = 0

                elif package_payment_tags == 'Self Pay':                            
                        amount = data.amount


                serialiser = AddToCartSerializer(get_data).data
                serialiser.update({'amount':amount})
                list_data.append(serialiser)

                # total_amount += float(amount)
                # platform_charge = float(math.ceil(total_amount * (0.02)))

                total_amount += math.ceil(float(amount))
                platform_charge = math.ceil(total_amount * 0.02)

                sgst = float(math.ceil(total_amount * (0.09)))
                cgst = float(math.ceil(total_amount * (0.09)))

            res = {
                'statuscode' : 200,
                'status':'true',
                'data':list_data,
                'total_amount':total_amount,
                'platform_charge':platform_charge,
                # 'sgst' : sgst,
                # 'cgst' : cgst,
                # 'grand_total': total_amount + sgst + cgst + platform_charge
                'grand_total': total_amount + platform_charge
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        
        
        
        elif user_type == 'individual':
            get_all_data = models.AddToCart.objects.filter(individual = id).order_by('-id')
            
            for data in get_all_data:
                # total_amount += float(data.amount)
                total_amount += math.ceil(float(data.amount))

            serialiser = AddToCartSerializer(get_all_data, many=True)
            # platform_charge = float(math.ceil(total_amount * (0.02)))
            platform_charge = math.ceil(total_amount * 0.02)
            sgst = float(math.ceil(total_amount * (0.09)))
            cgst = float(math.ceil(total_amount * (0.09)))

            res = {
                'statuscode' : 200,
                'status':'true',
                'data':serialiser.data,
                'total_amount':total_amount,
                'platform_charge':platform_charge,
                # 'sgst' : sgst,
                # 'cgst' : cgst,
                # 'grand_total': total_amount + sgst + cgst + platform_charge
                'grand_total': total_amount + platform_charge

            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message':'Enter valid User Type.'
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')




@csrf_exempt
def add_to_cart_count(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        user_type = python_data.get('user_type')
        id = python_data.get('id')


        if user_type == 'employee':
            count = models.AddToCart.objects.filter(employee = id).count()

            res = {
                'statuscode' : 200,
                'status':'true',
                'count':count,

            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
            
        elif user_type == 'individual':
            count = models.AddToCart.objects.filter(individual = id).count()
                                                     
            res = {
                'statuscode' : 200,
                'status':'true',
                'count':count,

            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message':'Enter valid User Type.'
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')






@csrf_exempt
def add_to_cart_delete(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')

        check_cart = models.AddToCart.objects.filter(id = id).count()
        if check_cart == 1:
            get_appointment = models.AddToCart.objects.filter(id = id).values_list('appointment', flat=True)[0]
            appointment = models.AppointmentDetail.objects.get(id = get_appointment)
            appointment.delete()
        
            # get_cart = models.AddToCart.objects.get(id = id)
            # get_cart.delete()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message':"Delete Package Successfully."
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
def add_to_card_transaction_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        flag = python_data.get('flag', 'employee')
        add_to_cart = python_data.get('add_to_cart')
        method = python_data.get('method', None)
        transaction_id = python_data.get('transaction_id', None)
        is_payment = python_data.get('is_payment')


        now = datetime.now()

        formatted_date = now.strftime("%B %d, %Y")
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        curr_time = time.strftime("%H:%M:%S", time.localtime())
        current_time = now.strftime("%Y%m%d%H%M%S")
        current_date_booking = now.strftime("%Y%m%d")

        if flag == 'employee':

            for cart in add_to_cart:
                cart = models.AddToCart.objects.get(id = cart)
                employee = cart.employee.id
                check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
                list_data = []
                if check_employee == 1:                    
                    package = cart.package.id
                    appointment = cart.appointment.id
                    patient = cart.patient.id
                    center = cart.appointment.center.id

                    type_of_visit = models.PackageDetail.objects.filter(id = package).values_list('type_of_visit', flat=True)[0]
                    appointment_create = models.AppointmentDetail.objects.get(id = appointment)
                    appointment_create.status = 'Request Received'
                    appointment_create.save()
                    appointment_id = appointment_create.id
                    appointment_date_1 = appointment_create.appointment_date_1
                    appointment_date_2 = appointment_create.appointment_date_2

                
                    package_data = models.PackageDetail.objects.get(id = package)
                    package_type = package_data.package_type
                    amount = package_data.offer_price
                    platform_charge = math.ceil(float(amount)*float(0.02))
                    total_amount = float(platform_charge) + float(amount)

                    corporate_id = models.EmployeeDetail.objects.filter(id = employee).values_list('corporate', flat=True)[0]

                    if is_payment == False:
                        amount = 0
                    ### Invoice Data
                    total_today_appointment = models.Transaction.objects.filter(created_at =current_date).count()
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
                        platform_charge = platform_charge,
                        total_amount = total_amount,
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

                    cart = models.AddToCart.objects.get(id = cart.id)
                    cart.delete()

                    recipient_name = appointment_create.patient.dependent_name
                    recipient_number = appointment_create.employee.mobile
                    recipient_email = appointment_create.employee.email
                    recipient_address = appointment_create.employee.address + ', ' + appointment_create.employee.city + ' - ' + appointment_create.employee.pincode

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

                            "package_name":package_name,
                            "package_service":package_service,
                            "package_amount":package_amount,
                            "package_discount_price":package_discount_price,
                            "amount_in_words":amount_in_words,
                            "package_offer_price":package_offer_price,
                            "platform_charge":platform_charge,
                            # "total_amount":total_amount,
                            "method":method,

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
                            "package_offer_price":total_amount,
                            "platform_charge":platform_charge,
                            # "total_amount":total_amount,

                            "flag":False,
                            "package_IGST":package_IGST,
                            "package_IGST_amount":package_IGST_amount,
                            "appointment_id":appointment_id
                        }
                    
                    data = createPDF(context)
                    
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'true',
                        'message' : "something went wrong.",
                        
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "You're appointment book successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        
        elif flag == 'individual':
          
            for cart in add_to_cart:
                cart = models.AddToCart.objects.get(id = cart)
                individual = cart.individual.id
                check_individual = models.IndividualUserDetail.objects.filter(id = individual).count()

                list_data = []
                if check_individual == 1:                    
                    package = cart.package.id
                    appointment = cart.appointment.id
                    patient = cart.individual_patient.id
                    center = cart.appointment.center.id

                    type_of_visit = models.PackageDetail.objects.filter(id = package).values_list('type_of_visit', flat=True)[0]
                    appointment_create = models.AppointmentDetail.objects.get(id = appointment)
                    appointment_create.status = 'Request Received'
                    appointment_create.save()
                    appointment_id = appointment_create.id
                    appointment_date_1 = appointment_create.appointment_date_1
                    appointment_date_2 = appointment_create.appointment_date_2

                    if is_payment == False:
                        amount = 0
                    ### Invoice Data
                    total_today_appointment = models.Transaction.objects.filter(created_at =current_date).count()
                    formatted_num = format(total_today_appointment, '03d')
                    all_appointment = models.AppointmentDetail.objects.all().count()
                    all_formatted_num = format(all_appointment, '05d')

                    booking_id = 'BKG-' + str(current_date_booking) + '-' +str(formatted_num)
                    
                    invoice_id = f'25-26/{formatted_num}/IN-{all_formatted_num}'

                    package_data = models.PackageDetail.objects.get(id = package)
                    package_type = package_data.package_type
                    amount = package_data.offer_price
                    platform_charge = math.ceil(float(amount)*float(0.02))
                    total_amount = float(platform_charge) + float(amount)

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
                    
                    cart = models.AddToCart.objects.get(id = cart.id)
                    cart.delete()
                    
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
                            "package_offer_price":total_amount,
                            "platform_charge":platform_charge,
                            # "total_amount":total_amount,


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
                            "package_offer_price":total_amount,
                            "platform_charge":platform_charge,
                            # "total_amount":total_amount,

                            "flag":False,
                            "package_IGST":package_IGST,
                            "package_IGST_amount":package_IGST_amount,
                            "appointment_id":appointment_id

                        }


                    data = createPDF(context)
                    
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'true',
                        'message' : "something went wrong.",
                        
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "You're appointment book successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 





@csrf_exempt
def user_data_svasthya(request):
    if request.method == "POST":
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
            action = python_data.get('Action', '')

            # If Action is GetAllData, return all employees without validation
            if action == 'GetAllData':
                page_number = int(python_data.get('PageNumber', 1))
                page_size = int(python_data.get('PageSize', 10))

                all_employees = models.EmployeeDetail.objects.all().order_by('id')
                start = (page_number - 1) * page_size
                end = start + page_size
                employees_page = all_employees[start:end]

                employee_serializer = EmployeeDetailSerializer(employees_page, many=True).data

                res = {
                    'statuscode': 200,
                    'status': 'true',
                    'user_data': employee_serializer,
                    'total_count': all_employees.count(),
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            # For other actions, validate required params
            required_params = ['Action', 'Username', 'Password', 'PageNumber', 'PageSize', 'CorporateCode', 'EmployeeCode']
            if not all(param in python_data and python_data[param] not in [None, '', 'null'] for param in required_params):
                res = {
                    'statuscode': 400,
                    'status': 'false',
                    'message': 'Missing or invalid required parameters.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            if action != 'GetBookingDatabyEmployeeCodeAndCorporateCode':
                res = {
                    'statuscode': 400,
                    'status': 'false',
                    'message': 'Invalid Action.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            corporate_code = python_data['CorporateCode']
            employee_code = python_data['EmployeeCode']

            try:
                get_user = models.EmployeeDetail.objects.get(
                    employee_code=employee_code,
                    hr_corporate_code=corporate_code
                )
            except models.EmployeeDetail.DoesNotExist:
                res = {
                    'statuscode': 406,
                    'status': 'false',
                    'message': 'User not found with provided CorporateCode and EmployeeCode.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            employee_serializer = EmployeeDetailSerializer(get_user).data

            appointment_detail = models.AppointmentDetail.objects.filter(employee=get_user.id)
            appointment_detail_serializer = AppointmentDetailEBPFSerializer(appointment_detail, many=True).data

            res = {
                'statuscode': 200,
                'status': 'true',
                'user_data': employee_serializer,
                'appointment_data': appointment_detail_serializer
            }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

        except Exception as e:
            import traceback
            traceback.print_exc()
            res = {
                'statuscode': 500,
                'status': 'false',
                'message': 'Internal server error.'
            }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

    else:
        res = {
            'statuscode': 405,
            'status': 'false',
            'message': 'Method not allowed.'
        }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')



@csrf_exempt
def booking_list_svasthya(request):
    if request.method == "POST":
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))

            action = python_data.get('Action', '')
            username = python_data.get('Username', '')
            password = python_data.get('Password', '')
            
            if username == "VIBPLAdmin" and password == "VIBPLAdmin@#$&*12345":

                # If Action is GetAllData, return all employees without validation
                if action == 'GetAllData':
                    page_number = int(python_data.get('PageNumber', 1))
                    page_size = int(python_data.get('PageSize', 10))

                    employee_data = models.AppointmentDetail.objects.filter(employee__employee_from ='EBPF').order_by('-id')

                    start = (page_number - 1) * page_size
                    end = start + page_size
                    employees_page = employee_data[start:end]

                    employee_serializer = AppointmentDetailEBPFSerializer(employees_page, many=True).data

                    res = {
                        'statuscode': 200,
                        'status': 'true',
                        'user_data': employee_serializer,
                        'total_count': employee_data.count(),
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
                
                else:
                    res = {
                        'statuscode': 400,
                        'status': 'false',
                        'message': 'Enter Valid action.'
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
            
            else:
                res = {
                    'statuscode': 400,
                    'status': 'false',
                    'message': 'Enter Valid user credntials.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

        except Exception as e:
            res = {
                'statuscode': 500,
                'status': 'false',
                'message': 'Internal server error.'
            }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
    else:
        res = {
            'statuscode': 405,
            'status': 'false',
            'message': 'Method not allowed.'
        }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')



@csrf_exempt
def address_select_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        flag = python_data.get('flag')
        id = python_data.get('id')
        if flag == 'employee':
            address = models.EmployeeAddressDetail.objects.get(id = id)
            employee = address.employee.id
            all_employee = models.EmployeeAddressDetail.objects.filter(employee = employee)
            for emp in all_employee:
                address_update = models.EmployeeAddressDetail.objects.get(id = emp.id)
                address_update.is_selected = False
                address_update.save()
            address.is_selected = True
            address.save()

        elif flag == 'individual':
            address = models.IndividualAddressDetail.objects.get(id = id)
            individual = address.individual.id
            all_employee = models.IndividualAddressDetail.objects.filter(individual = individual)
            for emp in all_employee:
                address_update = models.IndividualAddressDetail.objects.get(id = emp.id)
                address_update.is_selected = False
                address_update.save()
            address.is_selected = True
            address.save()

    res = {
        'statuscode' : 200,
        'status':'true',
        'message':'Address added successfully.',
        }
    json_data = JSONRenderer().render(res)
    return HttpResponse(json_data, content_type= 'application/json') 



