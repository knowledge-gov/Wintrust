from collections import namedtuple
import random
from home.views import register, index
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, response
from home.models import Register
from django.db import connection, transaction
from .models import Security,Beneficiary, Transaction, CardDetails

import smtplib,datetime
from email.message import EmailMessage


# Create your views here.






def index2(request):
    return render(request,'signin.html')


def auth(request):
    user = request.POST['userId']
    query = connection.cursor()
    query.execute("SELECT * FROM home_Register WHERE userid = %s ", [user])
    row = namedtuplefetchall(query)

    if row:
        for data in row:
            email = data.email
        sendmail(email)
        error = [
            'An extra layer of security is needed to complete this request.'
        ]
        data = {
            'row': row,
            'error' : error
        }
        return render(request,'Auth.html',{'context': data })
    else:
        return render(request,'signin.html',{'error': 'The UserId supplied is not associated with any account.'})



def beneficiary(request):
    query = connection.cursor()
    if 'user_id' in request.session:
        userid = request.session['user_id']

        if  'type' in request.POST :
            acctType = request.POST['type']
            accountNo = request.POST['accountNo']
            routineNo = request.POST['routineNo']
            name = request.POST['name']
            
            
            Save = Beneficiary()
            Save.name = name
            Save.acct_no = accountNo
            Save.routine_no = routineNo
            Save.type = acctType
            Save.user_id = userid

            Save.save()

            query.execute("SELECT * FROM home_Register WHERE userid = %s", [userid]);
            data_row = namedtuplefetchall(query)

            query.execute("SELECT name FROM banking_Beneficiary WHERE user_id = %s", [userid]);
            row = namedtuplefetchall(query)

            other1=[
                'Beneficiary Added Successfully'
            ]

            data={
                    'row_data':data_row,
                    'row':row,
                    'other1': other1
            }
            return render(request, 'bankTransfer.html',{'context':data})
        else:
            if  'amount' in request.POST :
                amount = request.POST['amount']
                holder = request.POST['holder']

                acct_no_debit= ''

                query.execute("SELECT * FROM home_Register WHERE userid = %s", [userid]);
                row = namedtuplefetchall(query)
                if row:
                    for data in row:
                        bal = data.balance
                    
                n_bal =  float(bal) - float(amount)

                Save = Transaction()
                Save.transcation_type = 'Debit'
                Save.amount = amount
                Save.prev_bal = bal
                Save.bal = n_bal
                Save.name = holder
                Save.user_id = userid
                Save.trans_date = datetime.datetime.now()
                Save.save()

                reg = Register.objects.get(userid = userid)
                reg.balance = n_bal
                reg.save()

                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                
                device_type = ""
                browser_type = ""
                browser_version = ""
                os_type = ""
                os_version = ""
                if request.user_agent.is_mobile:
                    device_type = "Mobile"
                if request.user_agent.is_tablet:
                    device_type = "Tablet"
                if request.user_agent.is_pc:
                    device_type = "PC"
                
                browser_type = request.user_agent.browser.family
                browser_version = request.user_agent.browser.version_string
                os_type = request.user_agent.os.family
                os_version = request.user_agent.os.version_string


                query.execute("SELECT * FROM home_Register WHERE userid = %s", [userid])
                data_row = namedtuplefetchall(query)
                if data_row:
                    for data in data_row:
                        email = data.email
                        acct_no_debit = data.account_No
                    senduserinfo(email,ip,device_type,browser_type,browser_version,os_type,os_version, amount, userid)

                query.execute("SELECT name FROM banking_Beneficiary WHERE user_id = %s", [userid])
                row = namedtuplefetchall(query)

                query.execute("SELECT * FROM banking_Transaction WHERE user_id = %s ORDER BY ID DESC LIMIT 1", [userid])
                success = namedtuplefetchall(query)
                s_name = ''
                s_amount = amount
                s_date = ''
                s_acctno=''
                s_routineno = ''
                ref = random.randint(100000000,999999999)

                if success:
                    for data in success:
                        s_name = data.name
                        s_date = data.trans_date

                query.execute("SELECT * FROM banking_Beneficiary WHERE name = %s ", [s_name] )
                success = namedtuplefetchall(query)
                if success:
                    for data in success:
                        s_acctno = data.acct_no
                        s_routineno = data.routine_no


                success={
                    'holder' :s_name,
                    'date': s_date,
                    'amount': s_amount,
                    'acct_no': s_acctno,
                    'routineno': s_routineno,
                    'ref': ref,
                    'acct_no_debit': acct_no_debit


                }

                data={
                        'row_data':data_row,
                        'row':row,
                        'success' :success
                    }
                return render(request, 'successful.html',{'context':data})
    else : 
        return render(request,'signin.html')



def transfer(request):
    query = connection.cursor()
    if  'user_id' in request.session :
        query = connection.cursor()
        user = request.session['user_id']
        query.execute("SELECT * FROM home_Register WHERE userid = %s ", [user])
        row_data = namedtuplefetchall(query)

        query.execute("SELECT name FROM banking_Beneficiary")
        row = namedtuplefetchall(query)

        data= {
            'row_data': row_data,
            'row': row
        }

        return render(request, 'bankTransfer.html', {'context': data})
    else:
        return render(request,'signin.html')



def linkcard(request):
    query = connection.cursor()
    if  'user_id' in request.session :
        user = request.session['user_id']
        if 'card_no' in request.POST:
            Save_card = CardDetails()
            Save_card.first_name = request.POST['first_name']
            Save_card.last_name = request.POST['last_name']
            Save_card.address = request.POST['address']
            Save_card.apt_unit = request.POST['apt']
            Save_card.card_number = request.POST['card_no']
            Save_card.expiry_date = request.POST['date']
            Save_card.city = request.POST['city']
            Save_card.state = request.POST['state']
            Save_card.cvv = request.POST['cvv']
            Save_card.user_id = user
            Save_card.zip_code = request.POST['zipcode']
            Save_card.save()
            other=[
                'Card Added Successffully, Your Dashboard will be updated Soon.'
            ]
            query.execute("SELECT * FROM home_Register WHERE userid = %s ", [user])
            row_data = namedtuplefetchall(query)

            data= {
                'row_data': row_data,
                'row': '',
                'other': other
            }

            return render(request,'linkCard.html',{'context': data})
        else:
            query.execute("SELECT * FROM home_Register WHERE userid = %s ", [user])
            row_data = namedtuplefetchall(query)

            data= {
                'row_data': row_data,
                'row': '',
                'other': ''
            }
            return render(request,'linkCard.html',{'context': data})
    else:
        return render(request,'signin.html')


def dash(request):
    query = connection.cursor()
    if  'user_id' in request.session :
        user = request.session['user_id']
        query.execute("SELECT * FROM home_Register WHERE userid = %s ", [user])
        row_data = namedtuplefetchall(query)

        query.execute("SELECT * FROM banking_Transaction WHERE user_id = %s  Order by id DESC LIMIT 5", [user])
        row = namedtuplefetchall(query)

        data={
                'row_data':row_data,
                'row':row,
                'other':''

        }

        return render(request,'dhome.html',{'context': data })
    else:
        return render(request,'signin.html')


def dashboard(request):
    if 'userId' in request.POST:
        user = request.POST['userId']
        otp = request.POST['otp']

        query = connection.cursor()
        query.execute("SELECT id FROM banking_Security WHERE otp = %s ", [otp])
        row = namedtuplefetchall(query)
        if row:
            query.execute("DELETE FROM banking_Security")
            query.execute("SELECT * FROM home_Register WHERE userid = %s ", [user])
            row_data = namedtuplefetchall(query)

            request.session['user_id'] = user

            query.execute("SELECT * FROM banking_Transaction WHERE user_id = %s  Order by id DESC LIMIT 5", [user])
            row = namedtuplefetchall(query)

            data={
                'row_data':row_data,
                'row':row,
                'other':'active'

            }

            query.execute("DELETE FROM banking_Security")

            return render(request,'dhome.html',{'context': data })
        else:
            query.execute("SELECT * FROM home_Register WHERE userid = %s ", [user])
            row = namedtuplefetchall(query)
            error = [
                'Invalid OTP'
            ]
            data = {
                'row':row,
                'error': error
            }
            return render(request,'Auth.html',{'context': data })
    else:
        return render(request,'signin.html')


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def sendmail(email):
    code = random.randint(100000,999999)
    save_content = Security()
    save_content.otp = code
    save_content.save()

    msg = EmailMessage()
    msg['Subject'] = 'New Registration'
    msg['From'] = 'wintrustbanking@gmail.com'
    msg['To'] = email 
    msg.set_content("Your Security Code is  " + str(code))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('wintrustbanking@gmail.com', 'vwrafgfpjitaplxl')#'avtltqidkrtbgvmz'
        smtp.send_message(msg)


def senduserinfo(email,ip,device_type,browser_type,browser_version,os_type,os_version,amount,userid):
    msg = EmailMessage()
    msg['Subject'] = 'Wintrust: Visitor Information'
    msg['From'] = 'wintrustbanking@gmail.com'
    msg['To'] = email 
    msg.set_content(
        "A transfer amount of  $" + amount + " has just been Processed by user " + userid + " \r"  
        "ip : " + ip + "\r"
        "device_type : " + device_type + "\r"
        "browser_type : " + browser_type + "\r"
        "browser_version : " + browser_version + "\r"
        "os_type : " + os_type + "\r"
        "os_version : "+ os_version
    )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('wintrustbanking@gmail.com', 'vwrafgfpjitaplxl')#'avtltqidkrtbgvmz'
        smtp.send_message(msg)

#query = connection.cursor()
#    query.execute("DELETE FROM banking_Security")