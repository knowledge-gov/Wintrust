from collections import namedtuple
import random
from home.views import register
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, response
from home.models import Register
from django.db import connection, transaction
from .models import Security,Beneficiary, Transaction

import smtplib
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

 

#def dashboard(request):
#    return render(request, 'dhome.html')


def beneficiary(request):
    query = connection.cursor()
    if  'type' in request.POST :
        acctType = request.POST['type']
        accountNo = request.POST['routineNo']
        routineNo = request.POST['routineNo']
        name = request.POST['name']

        save_content = Beneficiary()
        save_content.type = acctType
        save_content.acct_no = accountNo
        save_content.routine_no = routineNo
        save_content.name = name
        save_content.save()

        query.execute("SELECT name FROM banking_Beneficiary")
        row = namedtuplefetchall(query)

        return render(request, 'bankTransfer.html', {'context': row})
    else:
        holder = request.POST['holder']
        amount = request.POST['amount']
        userid = request.POST['userid']
        
        query.execute("SELECT * FROM home_Register WHERE userid = %s", [userid]);
        row = namedtuplefetchall(query)
        if row:
            for data in row:
                bal = data.balance

        Save = Transaction()
        Save.transcation_type = 'Debit'
        Save.amount = amount
        Save.name = holder
        Save.prev_bal = bal
        Save.bal = bal - amount
        Save.save()

        return render(request, 'bankTransfer.html')


def transfer(request):
    query = connection.cursor()
    query.execute("SELECT name FROM banking_Beneficiary")
    row = namedtuplefetchall(query)

    return render(request, 'bankTransfer.html', {'context': row})




def dashboard(request):
    user = request.POST['userId']
    otp = request.POST['otp']

    query = connection.cursor()
    query.execute("SELECT id FROM banking_Security WHERE otp = %s ", [otp])
    row = namedtuplefetchall(query)
    if row:
        query.execute("DELETE FROM banking_Security")
        query.execute("SELECT * FROM home_Register WHERE userid = %s ", [user])
        row_data = namedtuplefetchall(query)
        return render(request,'dhome.html',{'context': row_data })
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
    msg['From'] = 'sodeeqsodeeq@gmail.com'
    msg['To'] = email 
    msg.set_content("Your Security Code is  " + str(code))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('sodeeqsodeeq@gmail.com', 'avtltqidkrtbgvmz')
        smtp.send_message(msg)
    

#query = connection.cursor()
#    query.execute("DELETE FROM banking_Security")