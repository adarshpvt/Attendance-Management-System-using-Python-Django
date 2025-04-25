from django.shortcuts import render,redirect,get_object_or_404
from amsapp.models import coursedb,facultydb,studentdb,notific
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from  frontend.models import studnt_signup,save_signup,student_leavedb,Attendance
from django.contrib import messages

import datetime

# Create your views here.
def adminpage(req):
    course=coursedb.objects.all()
    c_course=course.count()
    faculty=facultydb.objects.all()
    c_faculty=faculty.count()
    student=studentdb.objects.all()
    c_student=student.count()
    ann=notific.objects.all()
    c_announcements=ann.count()
    times=datetime.datetime.now()
    return render(req,"admin.html",{'times':times,'c_course':c_course,'times':times,'c_faculty':c_faculty,'c_student':c_student,'c_announcements':c_announcements})

def add_course(req):



    return render(req,"add_course.html")
def save_course(req):
    if req.method == "POST":

        a = req.POST.get('cname')
        b = req.POST.get('bname')

        obj = coursedb(name=a,bname=b)
        obj.save()
        return redirect(add_course)
def view_course(req):
    course=coursedb.objects.all()
    return render(req,"view_course.html",{'course':course})
def edit_course(req,c_id):
    cou = coursedb.objects.get(id=c_id)

    return render(req,"edit_course.html",{'cou':cou,})
def edit_course(request, pk):
    course = get_object_or_404(coursedb, pk=pk)  # Retrieve the course by ID
    if request.method == 'POST':
        # Update course data with POST data
        course.name = request.POST.get('name')
        course.bname = request.POST.get('bname')

        course.save()  # Save changes
        return redirect('course_list')  # Redirect after saving
    # Pass course data to pre-fill the form
    return render(request, 'edit_course.html', {'course': course})
def update_course(req,co_id):
    if req.method=="POST":
        a = req.POST.get('cname')
        b = req.POST.get('bname')

    coursedb.objects.filter(id=co_id).update(name=a,bname=b)
    return redirect(view_course)
def delete_course(req,c_id):
    x=coursedb.objects.filter(id=c_id)
    x.delete()
    return redirect(view_course)
def add_faculty(req):
    cou=coursedb.objects.all()
    return render(req,"add_faculty.html",{'cou':cou})
def save_faculty(req):
    if req.method == "POST":
        a = req.POST.get('fname')
        b = req.POST.get('id')
        c = req.POST.get('cname')
        d = req.POST.get('bname')
        e = req.POST.get('f_gen')
        f = req.POST.get('f_dob')
        g = req.POST.get('fphn')
        h = req.POST.get('femail')
        i = req.POST.get('fdes')
        j = req.FILES['fimage']
        obj = facultydb(f_name=a,f_id=b,course_name=c,batch_name=d,f_gender=e,f_dob=f,f_phn=g,f_email=h,f_add=i,f_pic=j)
        obj.save()
        return redirect(add_faculty)
def view_faculty(req):
    fac=facultydb.objects.all()
    return render(req,"view_faculty.html",{'fac':fac})
def edit_faculty(req,f_id):
    cou = coursedb.objects.all()
    fac = facultydb.objects.get(id=f_id)
    return render(req,"edit_faculty.html",{'fac':fac,'cou':cou})
def update_faculty(req,f_id):
    if req.method=="POST":
        a = req.POST.get('fname')
        b = req.POST.get('id')
        c = req.POST.get('cname')
        d = req.POST.get('bname')
        e = req.POST.get('f_gen')
        f = req.POST.get('f_dob')
        g = req.POST.get('fphn')
        h = req.POST.get('femail')
        i = req.POST.get('fdes')
    try:
        j = req.FILES['fimage']
        fs=FileSystemStorage()
        file=fs.save(j.name,j)
    except MultiValueDictKeyError:
        file=facultydb.objects.get(id=f_id).f_pic
    facultydb.objects.filter(id=f_id).update(f_name=a,f_id=b,course_name=c,batch_name=d,f_gender=e,f_dob=f,f_phn=g,f_email=h,f_add=i,f_pic=file)
    return redirect(view_faculty)
def delete_faculty(req,f_id):
    x=facultydb.objects.filter(id=f_id)
    x.delete()
    return redirect(view_faculty)


def add_student(req):
    cou = coursedb.objects.all()
    fac = facultydb.objects.all()

    return render(req,"add_student.html",{'cou':cou,'fac':fac})

def save_student(req):
    if req.method == "POST":
        a = req.POST.get('sname')
        b = req.POST.get('sid')
        c = req.POST.get('cname')
        d = req.POST.get('bname')
        e = req.POST.get('sgender')
        f = req.POST.get('sdob')
        g = req.POST.get('sphn')
        h = req.POST.get('semail')
        i = req.POST.get('sdes')
        j = req.POST.get('p_email')
        l=req.POST.get('fname')
        k=req.FILES['simage']
        obj = studentdb(s_name=a,s_id=b,c_name=c,b_name=d,s_gender=e,s_dob=f,s_phn=g,s_email=h,s_add=i,sp_email=j,s_pic=k,s_fac=l)
        obj.save()
        return redirect(add_student)

def view_student(req):
    stud=studentdb.objects.all()
    return render(req,"view_student.html",{'stud':stud})




def edit_student(req,s_id):
    stud = studentdb.objects.get(id=s_id)
    fac=facultydb.objects.all()
    cou = coursedb.objects.all()
    return render(req,"edit_student.html",{'stud':stud,'fac':fac,'cou':cou})
def update_student(req,s_id):
    if req.method=="POST":
        a = req.POST.get('sname')
        b = req.POST.get('sid')
        c = req.POST.get('fname')
        d = req.POST.get('cname')
        e = req.POST.get('bname')
        f = req.POST.get('sgender')
        g = req.POST.get('sdob')
        h = req.POST.get('sphn')
        i = req.POST.get('semail')
        j = req.POST.get('sdes')
        k = req.POST.get('p_email')


    try:
        l = req.FILES['simage']
        fs=FileSystemStorage()
        file=fs.save(l.name,l)
    except MultiValueDictKeyError:
        file=studentdb.objects.get(id=s_id).s_pic
    studentdb.objects.filter(id=s_id).update(s_name=a,s_id=b,s_fac=c,c_name=d,b_name=e,s_gender=f,s_dob=g,s_phn=h,s_email=i,s_add=j,sp_email=k,s_pic=file)
    messages.success(req, 'Student details updated successfully!')
    return redirect(view_student)
def delete_student(req,s_id):
    x=studentdb.objects.filter(id=s_id)
    x.delete()
    return redirect(view_student)
def add_announcements(req):
    fac=facultydb.objects.all()
    return render(req,"add_notifications.html",{'fac':fac})
def View_Announcments(req):
    noti=notific.objects.all()
    return render(req,"View_Announcments.html",{'noti':noti})
def Save_Announcements(req):
    if req.method=="POST":
        a=req.POST.get('msg')
        b=req.POST.get('create')
        c=req.POST.get('facname')

        obj = notific(notificat=a,created=b,facult_name=c)
        obj.save()
        return redirect(add_announcements)
def edit_announcements(req,a_id):
    no = notific.objects.get(id=a_id)
    fac=facultydb.objects.all()
    return render(req,"edit_announcements.html",{'no':no,'fac':fac})
def update_announcements(req,an_id):
    if req.method=="POST":
        a = req.POST.get('msg')
        b = req.POST.get('create')
        c = req.POST.get('facname')

    notific.objects.filter(id=an_id).update(notificat=a,created=b,facult_name=c)
    return redirect(View_Announcments)
def delete_announcements(req,an_id):
    x=notific.objects.filter(id=an_id)
    x.delete()
    return redirect(View_Announcments)


def add_studentsignup(req):
    return render(req,"add_studentsignup.html")

def add_teacherignup(req):
    return render(req,"add_teachersignup.html")


def add_student_leave(req):
    cou=coursedb.objects.all()
    fac=facultydb.objects.all()
    return render(req,"add_student_leave.html",{'cou':cou,'fac':fac})

def add_studattendance(req):
    cou = coursedb.objects.all()
    fac = facultydb.objects.all()
    return render(req,"add_studattendance.html",{'cou':cou,'fac':fac})


def view_studentsignup(req):
    ss=studnt_signup.objects.all()
    return render(req,"view_studentsignup.html",{'ss':ss})

def view_teachersignup(req):
    ts=save_signup.objects.all()
    return render(req,"view_teachersignup.html",{'ts':ts})

def view_studentleave(req):
    sl=student_leavedb.objects.all()
    return render(req,"view_studentleave.html",{'sl':sl})

def view_studenattendence(req):
    sa=Attendance.objects.all()
    return render(req,"view_studentattendence.html",{'sa':sa})

def save_student_signup(req):
    if req.method == "POST":

        a = req.POST.get('sname')
        b = req.POST.get('semail')
        c = req.POST.get('spassword')
        d = req.POST.get('srepass')

        obj = studnt_signup(studnt_name=a,studnt_email=b,studnt_pass=c,studnt_repass=d)
        obj.save()
        return redirect(add_studentsignup)
def edit_student_signup(req,ss_id):
    std = studnt_signup.objects.get(id=ss_id)

    return render(req,"edit_student_signup.html",{'std':std,})

def update_student_signup(req,ss_id):
    if req.method=="POST":
        a = req.POST.get('sname')
        b = req.POST.get('semail')
        c = req.POST.get('spassword')
        d = req.POST.get('srepass')


    studnt_signup.objects.filter(id=ss_id).update(studnt_name=a,studnt_email=b,studnt_pass=c,studnt_repass=d)
    return redirect(view_studentsignup)
def delete_student_signup(req,ss_id):
    x=studnt_signup.objects.filter(id=ss_id)
    x.delete()
    return redirect(view_studentsignup)


def save_teacher_signup(req):
    if req.method == "POST":

        a = req.POST.get('tname')
        b = req.POST.get('temail')
        c = req.POST.get('tpass')
        d = req.POST.get('trepass')

        obj = save_signup(t_name=a,t_email=b,t_pass=c,t_repass=d)
        obj.save()
        return redirect(add_teacherignup)

def edit_teacher_signup(req,ts_id):
    tea = save_signup.objects.get(id=ts_id)

    return render(req,"edit_teacher_signup.html",{'tea':tea})


def update_teacher_signup(req,ts_id):
    if req.method=="POST":
        a = req.POST.get('tname')
        b = req.POST.get('temail')
        c = req.POST.get('tpass')
        d = req.POST.get('trepass')


    save_signup.objects.filter(id=ts_id).update(t_name=a,t_email=b,t_pass=c,t_repass=d)
    return redirect(view_teachersignup)
def delete_teacher_signup(req,ts_id):
    x=save_signup.objects.filter(id=ts_id)
    x.delete()
    return redirect(view_teachersignup)


def save_student_leave(request):
    if request.method == "POST":
        student_name = request.POST.get('lsname')
        course_name = request.POST.get('lcname')
        faculty_name = request.POST.get('lfname')
        leave_date = request.POST.get('date')
        leave_reason = request.POST.get('lreason')

        # Save to database
        obj = student_leavedb(
            l_sname=student_name,
            l_cname=course_name,
            l_fname=faculty_name,
            l_ndate=leave_date,
            l_reason=leave_reason,
            status='Pending'  # Default status
        )
        obj.save()

        messages.success(request, "Leave request submitted successfully.")
        return redirect(add_student_leave)
def edit_studentleave(req,sl_id):
    sleave = student_leavedb.objects.get(id=sl_id)
    cou = coursedb.objects.all()
    fac = facultydb.objects.all()

    return render(req,"edit_studentleave.html",{'sleave':sleave,'cou':cou,'fac':fac})

def edit_studentattend(req,sa_id):
    satt = Attendance.objects.get(id=sa_id)
    cou = coursedb.objects.all()
    fac = facultydb.objects.all()

    return render(req,"edit_studentattend.html",{'satt':satt,'cou':cou,'fac':fac})


def update_studentleave(request,sl_id):
    if request.method=="POST":
        student_name = request.POST.get('lsname')
        course_name = request.POST.get('lcname')
        faculty_name = request.POST.get('lfname')
        leave_date = request.POST.get('date')
        leave_reason = request.POST.get('lreason')

        # Save to database
        student_leavedb.objects.filter(id=sl_id).update(
            l_sname=student_name,
            l_cname=course_name,
            l_fname=faculty_name,
            l_ndate=leave_date,
            l_reason=leave_reason,
            status='Pending'  # Default status
        )


    return redirect(view_studentleave)

def delete_student_leave(req,sl_id):
    x=student_leavedb.objects.filter(id=sl_id)
    x.delete()
    return redirect(view_studentleave)

def delete_studentattendance(req,sa_id):
    x=Attendance.objects.filter(id=sa_id)
    x.delete()
    return redirect(view_studenattendence)

def save_studattendance(request):
    if request.method == 'POST':
        course_name = request.POST.get('course-name')
        batch_name = request.POST.get('batch-name')
        faculty_name = request.POST.get('faculty-name')
        attendance_date = request.POST.get('attendance-date')
        student_id = request.POST.get('student-id')
        student_name = request.POST.get('student-name')
        status = request.POST.get('attendance-status')

        # Check if an attendance record already exists for the student on the same date
        if Attendance.objects.filter(student_id=student_id, attendance_date=attendance_date).exists():
            messages.error(request, "Attendance for this student on this date already exists.")
        else:
            # Save new attendance record
            obj = Attendance(
                course_name=course_name,
                batch_name=batch_name,
                faculty_name=faculty_name,
                attendance_date=attendance_date,
                student_id=student_id,
                student_name=student_name,
                status=status
            )
            obj.save()
            messages.success(request, "Attendance saved successfully!")

        return redirect(add_studattendance)
def logins(req):
    return render(req,"login.html")

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ' Admin Successfully logged in!')
            return redirect(adminpage)  # Redirect to the admin dashboard
        else:
            messages.error(request, 'Invalid credentials! Please check your username and password.')

    return render(request, 'login.html')
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def check_username(request):
    """ Check if the username exists in the database """
    if request.method == "POST":
        username = request.POST.get("username")
        exists = User.objects.filter(username=username).exists()
        return JsonResponse({"exists": exists})

@csrf_exempt
def validate_login(request):
    """ Validate username and password """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        return JsonResponse({"valid": bool(user)})



from django.contrib.auth import logout

def delete_logout(request):
        logout(request)  # Log out the user
        messages.success(request, 'You have been logged out successfully.')  # Set a success message

        return redirect(admin_login)
