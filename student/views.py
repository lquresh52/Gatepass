from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from student.models import stu_signup,in_req
import psycopg2
import datetime
from datetime import date
import os
from django.conf import settings
from django.core.mail import send_mail

numalpha='abcdefghijklmnopqrstuvwxyz0123456789'
key=5


# Create your views here.

#************************************************************************************************************************************
def index(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')
    else:
        auth.logout(request)
        return redirect('/')

#************************************************************************************************************************************

def about_us(request):
    if request.method == 'POST':
        return render(request,'about_us.html') 
    else:
        return render(request,'about_us.html')

#************************************************************************************************************************************

def student_login(request):
    if request.method == 'POST':
        username=request.POST.get("username")
        password=request.POST.get("password")

        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute("select valid from student_stu_signup where username='"+ username +"'")
        valid=cur.fetchall()
        print(valid)

        if (any('Pending' in i for i in valid)):
            print('Pending')
            messages.info(request,'Plz contact your respective GFM for validating your account')
            return redirect('student_login')

        elif (any('rejected' in i for i in valid)):
            print('rejected')
            messages.info(request,'Your account has been rejected')
            return redirect('student_login')

        else:
            if username is not None:
                cur.execute("select username,password from student_stu_signup where username='"+ username +"'")
                rows=cur.fetchall()
                if rows==[]:
                    messages.info(request,'User not exists!')
                    return redirect("student_login")
                else:
                    for r in rows:
                        decrypt=''
                        pas=r[1]
                        for i in pas:
	                        posi=numalpha.find(i)
	                        newposi=(posi-key)%36
	                        decrypt=decrypt+numalpha[newposi]

                        if r[0]==username and decrypt==password :
                            print(r)
                            # con.close()
                            # user=auth.authenticate(username=username,password=password)
                            user = authenticate(request, username=username, password=password)
                            print(user)
                            if user is not None:
                                auth.login(request, user)
                                return redirect("stu_home")
                            else:
                                return redirect("student_login")
                        else:         
                            print("out")
                            print(r)
                            messages.info(request,'Username or Password not matched!')
                            con.close()
                            return redirect("student_login")
            else:
                return render(request,'stu_login.html')
            print(rows)
            con.close()
            return redirect('student_login') 
    else:
        return render(request,'stu_login.html')


#************************************************************************************************************************************


def signup_form(request):
    if request.method=='POST':
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        gender=request.POST.get('gender')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        email=request.POST.get('email')
        mobile_no=request.POST.get('mobile_no')
        year=request.POST.get('year')
        branch=request.POST.get('branch')
        roll_no=request.POST.get('roll_no')
        gfm=request.POST.get('gfm')
        # icard_img=request.POST.get('icard_img')
        # p=request.POST.get('icard_img')
        p=request.FILES['icard_img']

        # user_img=request.POST.get('user_img')
        p1=request.FILES['user_img']

        print(type(p))

        print(p1)
        print(p)
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        # cur=con.cursor()
        # cur.execute("select username from park_signup where username='" + username + "'")
        # rows=cur.fetchall()
        
        if User.objects.filter(username=username).exists():
            messages.info(request,'User name taken')
            return redirect('signup_form')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email id already in use')
            return redirect('signup_form')
        elif password1!=password2:
            messages.info(request,'Password did not match')
            return redirect('signup_form')
        elif not int(roll_no) > 0:
            messages.info(request,'Invalid Roll number')
            return redirect('signup_form')
        else:
            encrypt=''
            for i in password1:
	            pos=numalpha.find(i)
	            newpos=(pos+key)%36
	            encrypt=encrypt+numalpha[newpos]
            user= stu_signup(username=username,first_name=first_name,last_name=last_name,gender=gender,password=encrypt,email=email,mobile_no=mobile_no,year=year,branch=branch,roll_no=roll_no,gfm=gfm,icard_img=p,user_img=p1,valid='Pending')
            user.save()
            # Authentication mate django user create kido
            user= User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
            user.save()
            print('registered')
            return redirect("student_login")
        
        return redirect('student_login')
    else:
        return render(request,'stu_signup.html')



#************************************************************************************************************************************


def forget_pass1(request):
    if request.method == 'POST':
        email=request.POST.get("email")
        mobile_no=request.POST.get("mobile_no")
        print(email,mobile_no)
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute("select email,mobile_no,valid from student_stu_signup where email='" + email + "' and mobile_no="+mobile_no+"")
        rows=cur.fetchall()
        con.close()
        print(rows)
        if not rows ==[]:
            for r in rows:
                if not r[2]=='rejected':
                    print(r[1])
                    if email == r[0] and int(mobile_no)==r[1]:
                        return redirect('forget_pass2')
                    else:
                        messages.info(request,'Email id and mobile number did not match!!!!!!!! ')
                        return render(request,'forget_pass1.html')
                else :
                    messages.info(request,'Your account has been rejected')
                    return render(request,'forget_pass1.html')
        # else:
        #     messages.info(request,'Email id and mobile number didn''t match ')
        #     return render(request,'forget_pass1.html')
    else:
        return render(request,'forget_pass1.html')
    

#************************************************************************************************************************************




def forget_pass2(request):
    print('lol')
    if request.method == 'POST':
        email=request.POST.get("email")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        
        print(email,password1,password2)
        
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")
        cur=con.cursor()
        
        print(len(password1),len(password2))
        
        if len(password1) == len(password2) and password1 == password2:
            print('inside update')
            encrypt=''
            for i in password1:
	            pos=numalpha.find(i)
	            newpos=(pos+key)%36
	            encrypt=encrypt+numalpha[newpos]


            u = User.objects.get(email=''+email+'')
            u.set_password(''+password1+'')
            u.save()
            print('//////////////  changed pass in AUTH-USER //////////////')
            print(u)

            cur.execute("update student_stu_signup set password='"+ encrypt +"' where email='"+email+"'")
            con.commit()
            con.close()
            return redirect('student_login')
        else:
            messages.info(request,'password and confirm password did not match')
            return redirect('forget_pass2')
    else:
        return render(request,'forget_pass2.html')
    
#************************************************************************************************************************************
# application='none'
@login_required(login_url='../student/student_login')
def stu_home(request):
    if request.method=='POST':
        return redirect('stu_home')
    else:
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")
        print('In student home')
        username=request.user.username
        print(username)
        cur=con.cursor()
        cur.execute("select apply_time,username,reason_des,status from student_in_req where username='" + username + "'")
        rows=cur.fetchall()
        
        # for generating  id number e.g 1,2,3,4 depend on rows
        new_row = list(rows)
        for i in range (0, len(rows)):
            new_row[i] = (i+1,) + new_row[i]

        print(new_row)
        return render(request,'stu_home.html',{'data':new_row})
        

#************************************************************************************************************************************


def logout(request):
    auth.logout(request)
    return redirect('student_login')



#************************************************************************************************************************************


@login_required(login_url='../student/student_login')
def in_apply(request):
    if request.method=='POST':
        reason=request.POST.get('radio')
        reason_des=request.POST.get('reason_des')
        # request_type=request.POST.get('Submit')
        print(reason,reason_des)
        now = datetime.datetime.now()
        username=request.user.username
        first_name = request.user.first_name
        last_name = request.user.last_name
        today = date.today()
        
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")
        cur=con.cursor()
        cur.execute("select mobile_no,email from student_stu_signup where username='" + username + "'")
        rows=cur.fetchall()
        email=''
        mobile_no=''
        if not rows==[]:
            for r in rows:
                email=r[1]
                mobile_no=int(r[0])


        cur.execute("select apply_time,in_req_count,req_date from student_in_req where username='" + username + "'")
        row=cur.fetchall()
        count=0
        req_date=''
        if not row==[]:
            for r in row:
                count=int(r[1])
                req_date=r[2]
        
        if today == req_date:
            print('//////////////////')
            if not count==1:
                #send_mail(subject,message,from_email,to_list,fail_silently=True)
                subject = 'There is a IN request by student : '+first_name+last_name+'.'
                message = 'REASON : '+reason+'\n REASON DESCRIPTION : '+reason_des
                from_email = settings.EMAIL_HOST_USER
                to_list = ['lquresh52@gmail.com']

                send_mail(subject , message , from_email , to_list , fail_silently=True)

                user=in_req(apply_time=datetime.datetime.now(), reason=reason, reason_des=reason_des, username=username, gmail=email, mobile_no=mobile_no, status='Pending',request_type='IN Request' , in_req_count=count+1 , req_date=today )
                user.save()
                print('data saved in table')



            else:
                messages.info(request,'Your daily limit for apply of gate pass is over contact your respective HOD sir')
                return redirect('in_apply')
        else:
            print('888888888888888')
            print(email,mobile_no)
            subject = 'There is a IN request by student : '+first_name+last_name+'.'
            message = 'REASON : '+reason+'\n REASON DESCRIPTION : '+reason_des
            from_email = settings.EMAIL_HOST_USER
            to_list = ['lquresh52@gmail.com']

            send_mail(subject , message , from_email , to_list , fail_silently=True)
            user=in_req(apply_time=str(datetime.datetime.now()), reason=reason, reason_des=reason_des, username=username, gmail=email, mobile_no=mobile_no, status='Pending',request_type='IN Request' , in_req_count=count+1 , req_date=today )
            user.save()
            print('data saved in table')

            # return render(request,'stu_home.html')
            return redirect('stu_home')
        return redirect('stu_home')
    else:
        return render(request,'in_apply.html')




#************************************************************************************************************************************

@login_required
def out_apply(request):
    if request.method=='POST':
        reason=request.POST.get('radio')
        reason_des=request.POST.get('reason_des')
        # request_type=request.POST.get('Submit')
        print(reason,reason_des)
        now = datetime.datetime.now()
        username=request.user.username
        first_name = request.user.first_name
        last_name = request.user.last_name
        today = date.today()
        
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")
        cur=con.cursor()
        cur.execute("select mobile_no,email from student_stu_signup where username='" + username + "'")
        rows=cur.fetchall()
        email=''
        mobile_no=''
        print(rows)
        if not rows==[]:
            for r in rows:
                email=r[1]
                mobile_no=int(r[0])


        cur.execute("select apply_time,out_req_count,req_date from student_in_req where username='" + username + "'")
        row=cur.fetchall()
        count=0
        req_date=''
        if not row==[]:
            for r in row:
                count=int(r[1])
                req_date=r[2]
        print(req_date)
        if today==req_date:
            print('//////////////////')
            if not count==1:
                subject = 'There is a OUT Request by student : '+first_name+last_name+'.'
                message = 'REASON : '+reason+'\n REASON DESCRIPTION : '+reason_des
                from_email = settings.EMAIL_HOST_USER
                to_list = ['lquresh52@gmail.com']

                send_mail(subject , message , from_email , to_list , fail_silently=True)
                user=in_req(apply_time=datetime.datetime.now(), reason=reason, reason_des=reason_des, username=username, gmail=email, mobile_no=mobile_no, status='Pending',request_type='Out Request' , out_req_count=count+1 , req_date=today )
                user.save()


            else:
                messages.info(request,'Your daily limit for apply of gate pass is over contact your respective HOD sir')
                return redirect('out_apply')
        else:
            print('888888888888888')
            print(email,mobile_no)
            subject = 'There is a OUT Request by student : '+first_name+last_name+'.'
            message = 'REASON : '+reason+'\n REASON DESCRIPTION : '+reason_des
            from_email = settings.EMAIL_HOST_USER
            to_list = ['lquresh52@gmail.com']

            send_mail(subject , message , from_email , to_list , fail_silently=True)
            user=in_req(apply_time=str(datetime.datetime.now()), reason=reason, reason_des=reason_des, username=username, gmail=email, mobile_no=mobile_no, status='Pending',request_type='Out Request' , out_req_count=count+1 , req_date=today )
            user.save()
            # return render(request,'stu_home.html')
            return redirect('stu_home')

        return redirect('stu_home')
    
    else:
        return render(request,'out_apply.html')
    
    
    
    # if request.method=='POST':
    #     return render(request,'out_apply.html')
    # else:
    #     return render(request,'out_apply.html')




#************************************************************************************************************************************

@login_required
def inout_apply(request):
    if request.method=='POST':

        return render(request,'inout_apply.html')
    else:
        return render(request,'inout_apply.html')




#************************************************************************************************************************************