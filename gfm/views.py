from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from . models import gfm_signup
import psycopg2
import datetime

numalpha='abcdefghijklmnopqrstuvwxyz0123456789'
key=5



# Create your views here.

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

def gfm_login(request):
    if request.method=='POST':
        gfm=request.POST.get('gfm')
        password=request.POST.get('password')

        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()

        cur.execute("select valid from gfm_gfm_signup where gfm='"+ gfm +"'")
        valid=cur.fetchall()
        
        if (any('Pending' in i for i in valid)):
            print('Pending')
            messages.info(request,'Plz contact HOD sir for validating your account')
            return redirect('gfm_login')
        else:
            if gfm is not None:
                cur.execute("select gfm,password from gfm_gfm_signup where gfm='"+ gfm +"'")
                rows=cur.fetchall()
                if rows==[]:
                    messages.info(request,'User not exists!')
                    return redirect("gfm_login")
                else:
                    for r in rows:
                        decrypt=''
                        pas=r[1]
                        for i in pas:
	                        posi=numalpha.find(i)
	                        newposi=(posi-key)%36
	                        decrypt=decrypt+numalpha[newposi]

                        if r[0]==gfm and decrypt==password :
                            print(r)
                            con.close()
                            user=auth.authenticate(username=gfm,password=password)
                            print(user)
                            if user is not None:
                                auth.login(request, user)
                                return redirect("gfm_home")
                            else:
                                return redirect("gfm_login")
                        else:         
                            print("out")
                            print(r)
                            messages.info(request,'Username or Password not matched!')
                            con.close()
                            return redirect("gfm_login")
            else:
                return render(request,'gfm_login.html')
            print(rows)
            con.close()
       
            print('approved')
            return redirect('gfm_home')
    else:
        return render(request,'gfm_login.html')

#************************************************************************************************************************************

def gfm_signup_form(request):
    if request.method=='POST':
        gfm=request.POST.get('gfm')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        mobile_no=request.POST.get('mobile_no')
        icard_no=request.POST.get('icard_no')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')

        if User.objects.filter(username=gfm).exists():
            messages.info(request,'User name taken')
            return redirect('gfm_signup_form')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email id already in use')
            return redirect('gfm_signup_form')
        elif password1!=password2:
            messages.info(request,'Password did not match')
            return redirect('gfm_signup_form')
        else:
            encrypt=''
            for i in password1:
	            pos=numalpha.find(i)
	            newpos=(pos+key)%36
	            encrypt=encrypt+numalpha[newpos]
            user= gfm_signup(gfm=gfm,first_name=first_name,last_name=last_name,password=encrypt,email=email,mobile_no=mobile_no,icard_no=icard_no,valid='Pending')
            user.save()
            # Authentication mate django user create kido
            user= User.objects.create_user(username=gfm,password=password1,email=email,first_name=first_name,last_name=last_name)
            user.save()
            print('registered')
            return redirect("gfm_login")
        return redirect('gfm_login')

    else:
        return render(request,'gfm_signup_form.html')
#************************************************************************************************************************************


def gfm_home(request):
    return render(request,'gfm_home.html')


#************************************************************************************************************************************

def gfm_rejected_stu(request):
    if request.method=='POST':
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        gen=request.POST.get('verify')
        per=request.POST.get('Submit')
        print("HEllo")
        print(per)
        print(gen)

        if per is not None:
            if gen == 'accept':
                cur.execute("update student_stu_signup set valid='accepted' where username='"+per+"'")
                con.commit()
            else:
                cur.execute("update student_stu_signup set valid='rejected' where username='"+per+"'")
                con.commit()
        con.close()
        return redirect('gfm_rejected_stu')
    else:
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        username=request.user.username
        print("/////////////////////////////")
        print(username)
        cur=con.cursor()
        cur.execute("select id,username,mobile_no,year,roll_no from student_stu_signup where valid='rejected' and gfm='"+username+"'")
        rows=cur.fetchall()
        if rows is not None:
            print(rows) 
            con.close()
            return render(request,'gfm_rejected_stu.html',{'data':rows})
        else:
            # return redirect('apply')
            return render(request,'gfm_rejected_stu.html')



#************************************************************************************************************************************

def gfm_grant_permission(request):
    if request.method=='POST':
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        gen=request.POST.get('verify')
        per=request.POST.get('Submit')
        print("HEllo")
        print(per)
        print(gen)

        date=str(datetime.datetime.now())
        today_date = str(datetime.date.today())
        print(date)
        print(today_date)

        if per is not None:
            if gen == 'accept':
                # cur.execute("update student_in_req set status='accepted',req_accept_time = '"+ dt_string +"' where username='"+per+"'")
                cur.execute("update student_in_req set status='accepted',req_accept_time='"+date+"' where username='"+per+"'and req_date='"+today_date+"' and status!='IN' and status!='OUT'")
                con.commit()
            else:
                # cur.execute("update student_in_req set status='rejected',req_accept_time='"+dt_string+"' where username='"+per+"'")
                cur.execute("update student_in_req set status='rejected',req_accept_time='"+date+"' where username='"+per+"'and req_date='"+today_date+"' and status!='IN' and status!='OUT'")
                con.commit()
        con.close()
        return redirect('gfm_grant_permission')

        # return render(request,'gfm_grant_permission.html')
    else:
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        cur.execute("select username,mobile_no,reason,reason_des,request_type from student_in_req where status='Pending'")
        rows=cur.fetchall()

        # for generating  id number e.g 1,2,3,4 depend on rows
        new_row = list(rows)
        for i in range (0, len(rows)):
            new_row[i] = (i+1,) + new_row[i]
        
        if rows is not None:
            print(rows) 
            con.close()
            return render(request,'gfm_grant_permission.html',{'data':new_row})
        else:
            # return redirect('apply')
            return render(request,'gfm_grant_permission.html')

        return render(request,'gfm_grant_permission.html')





#************************************************************************************************************************************

def gfm_validate_stu(request):
    if request.method=='POST':
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        cur=con.cursor()
        gen=request.POST.get('verify')
        per=request.POST.get('Submit')
        print("HEllo")
        print(per)
        print(gen)

        if per is not None:
            if gen == 'accept':
                cur.execute("update student_stu_signup set valid='accepted' where username='"+per+"'")
                con.commit()
            else:
                cur.execute("update student_stu_signup set valid='rejected' where username='"+per+"'")
                con.commit()
        con.close()
        return redirect('gfm_validate_stu')
    else:
        con=psycopg2.connect(
            host="localhost",
            database="gatepass",
            user="postgres",
            password="123456")

        username=request.user.username
        cur=con.cursor()
        cur.execute("select id,username,mobile_no,year,roll_no from student_stu_signup where valid='Pending' and gfm='"+username+"'")
        rows=cur.fetchall()
        if rows is not None:
            print(rows) 
            con.close()
            return render(request,'gfm_validate_stu.html',{'data':rows})
        else:
            # return redirect('apply')
            return render(request,'gfm_validate_stu.html')


    # return render(request,'gfm_validate_stu.html')

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
        cur.execute("select email,mobile_no,valid from gfm_gfm_signup where email='" + email + "' and mobile_no="+mobile_no+"")
        rows=cur.fetchall()
        con.close()
        print(rows)
        if not rows ==[]:
            for r in rows:
                if not r[2]=='rejected':
                    print(r[1])
                    if email == r[0] and int(mobile_no)==r[1]:
                        return redirect('forget_pass')
                    else:
                        messages.info(request,'Email id and mobile number did not match!!!!!!!! ')
                        return render(request,'forget_pass1.html')
                else :
                    messages.info(request,'Your account has been rejected')
                    return render(request,'forget_pass1.html')
        else:
            return redirect('forget_pass1')
    else:
        return render(request,'forget_pass1.html')
    

#************************************************************************************************************************************




def forget_pass(request):
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
            cur.execute("update gfm_gfm_signup set password='"+ encrypt +"' where email='"+email+"'")
            con.commit()
            con.close()
            return redirect('gfm_login')
        else:
            messages.info(request,'password and confirm password did not match')
            return redirect('forget_pass2')
    else:
        return render(request,'forget_pass2.html')


#************************************************************************************************************************************
def logout(request):
    auth.logout(request)
    return redirect('/')