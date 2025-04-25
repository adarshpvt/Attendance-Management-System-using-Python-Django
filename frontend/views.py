from django.shortcuts import render,redirect,get_object_or_404
from amsapp.models import facultydb,coursedb,studentdb,notific
from frontend.models import save_signup,Attendance,studnt_signup,student_leavedb
import datetime
from datetime import datetime
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Count, Q


def home(request):
    course = coursedb.objects.all()
    ctime = datetime.now()
    today_date = now().date()

    # Get faculty details from session
    faculty_name = request.session.get('f_name', '').strip()  # Remove extra spaces
    course_name = request.session.get('course_name', '').strip()
    batch_name = request.session.get('batch_name', '').strip()

    if not faculty_name:
        return render(request, "index.html", {
            'course': course,
            'ctime': ctime,
            'error': "Please log in first"
        })

    # Filter students under the logged-in faculty
    students_query = studentdb.objects.filter(
        s_fac__iexact=faculty_name, c_name__iexact=course_name, b_name__iexact=batch_name
    )

    # Get batch strength
    batch_strength = students_query.count()

    # Ensure faculty name exactly matches in attendance database
    attendance_marked = Attendance.objects.filter(
        Q(faculty_name__iexact=faculty_name) &
        Q(course_name__iexact=course_name) &
        Q(batch_name__iexact=batch_name) &
        Q(attendance_date=today_date)
    ).exists()

    # Count present students if attendance is marked
    present_count = 0
    if attendance_marked:
        present_count = Attendance.objects.filter(
            faculty_name__iexact=faculty_name, course_name__iexact=course_name, batch_name__iexact=batch_name,
            attendance_date=today_date, status__iexact="Present"  # Match case-insensitively
        ).count()

    teacher_details = {
        'f_name': faculty_name,
        'f_id': request.session.get('f_id'),
        'course_name': course_name,
        'batch_name': batch_name,
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }
    faculty_name = request.session.get('f_name')

    if not faculty_name:
        return render(request, "index.html", {'error': "Faculty not logged in."})

    # Get students under this faculty
    students = studentdb.objects.filter(s_fac=faculty_name)

    # Extract student IDs
    student_ids = students.values_list('s_id', flat=True)

    # Get attendance records for these students
    attendance_records = Attendance.objects.filter(student_id__in=student_ids)

    # Initialize count for low attendance students
    low_attendance_count = 0

    # Calculate attendance percentage for each student
    student_attendance = {}

    for student in students:
        student_id = student.s_id
        student_name = student.s_name

        total_classes = attendance_records.filter(student_id=student_id).count()
        present_classes = attendance_records.filter(student_id=student_id, status__iexact="Present").count()

        if total_classes > 0:
            attendance_percentage = round((present_classes / total_classes) * 100, 2)
        else:
            attendance_percentage = 0

        if attendance_percentage < 75:
            low_attendance_count += 1  # Count students with low attendance

        student_attendance[student_id] = {
            'student_name': student_name,
            'total_classes': total_classes,
            'total_present': present_classes,
            'attendance_percentage': attendance_percentage,
        }

    return render(request, "index.html", {
        'course': course,
        'ctime': ctime,
        'teacher_details': teacher_details,
        'batch_strength': batch_strength,
        'attendance_marked': attendance_marked,
        'present_count': present_count,
        'students': students_query,
        'today_date':today_date,
        'low_attendance_count': low_attendance_count,
        'student_attendance': student_attendance,
    })





def student(request):
    ctime = datetime.now()
    teacher_details = {
        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }
    course = coursedb.objects.all()

    return render(request,"student.html",{'course':course,'teacher_details':teacher_details,'ctime':ctime})
def save_Tstudent(req):
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
        k=req.FILES['simage']
        obj = studentdb(s_name=a,s_id=b,c_name=c,b_name=d,s_gender=e,s_dob=f,s_phn=g,s_email=h,s_add=i,sp_email=j,s_pic=k)
        obj.save()
        return redirect(student)
def fac(request):
    ctime =datetime.datetime.now()
    teacher_details = {
        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }
    return render(request,"fac.html",{{'teacher_details':teacher_details,'ctime':ctime}})
def view_students(request):
    logged_in_faculty_name = request.session.get('f_name')  # Assuming faculty name is stored in session

    # Count students registered under this faculty
    student = studentdb.objects.filter(s_fac=logged_in_faculty_name)
    ctime =datetime.now()
    courses = coursedb.objects.all()
    teacher_details = {
        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }
    return render(request,"view_students.html",{'student':student,'courses':courses,'teacher_details':teacher_details,'ctime':ctime})

def mark_attendance(request):
    today = datetime.today()
    ctime = today.strftime("%d/%m/%Y")
    courses = coursedb.objects.all()
    batch = facultydb.objects.all()
    teacher_details = {
        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }
    return render(request,"mark_attendance.html",{'courses':courses,'ctime': ctime,'batch':batch,'teacher_details':teacher_details})


def save_attendance(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        batch_name = request.POST.get('batch_name')
        faculty_name = request.POST.get('faculty_name')
        attendance_date = request.POST.get('attendance_date')

        # Loop through each student ID and save their attendance status
        student_ids = [key.split('_')[2] for key in request.POST if key.startswith('attendance_status_')]

        for student_id in student_ids:
            # Get the student's name (assuming you have it in the context)
            student_name = request.POST.get(f'student_name_{student_id}')  # Adjust this if necessary

            # Check if the student is present or absent
            present_status = request.POST.get(f'attendance_status_{student_id}') == 'Present'
            absent_status = request.POST.get(f'attendance_status_{student_id}') == 'Absent'

            if present_status:
                # Save present status
                Attendance.objects.create(
                    course_name=course_name,
                    batch_name=batch_name,
                    faculty_name=faculty_name,
                    attendance_date=attendance_date,
                    student_id=student_id,
                    student_name=student_name,  # Save the student's name
                    status='Present'
                )
            elif absent_status:
                # Save absent status
                Attendance.objects.create(
                    course_name=course_name,
                    batch_name=batch_name,
                    faculty_name=faculty_name,
                    attendance_date=attendance_date,
                    student_id=student_id,
                    student_name=student_name,  # Save the student's name
                    status='Absent'
                )
            else:
                # If neither is checked, you can choose to handle it (e.g., log a warning, skip saving, etc.)
                continue

        return redirect(home)  # Redirect to a success page or another view


def editstudents(request,s_id):
    cou = coursedb.objects.all()
    ctime =datetime.datetime.now()
    studs = studentdb.objects.get(id=s_id)
    teacher_details = {
        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }
    return render(request,"edit_students.html",{'ctime':ctime,'studs':studs,'cou':cou,'teacher_details':teacher_details})


def signin(req):
    return render(req,"signin.html")
def view_batches(request):
    ctime =datetime.now()
    batch=facultydb.objects.all()
    teacher_details = {
        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }
    return render(request,"view_batches.html",{'ctime':ctime,'batch':batch,'teacher_details':teacher_details})

def course_filter(request, cou_name):
    ctime =datetime.now()
    batch = facultydb.objects.all()
    data = studentdb.objects.filter(c_name=cou_name)
    course_name = cou_name
    batch_name = data[0].b_name
    faculty_name = data[0].s_fac
    teacher_details = {
        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }

    return render(request, "view_class.html", {
        'data': data,
        'batch': batch,
        'course_name': course_name,
        'batch_name': batch_name,
        'faculty_name': faculty_name,'teacher_details':teacher_details,
        'ctime':ctime
    })

from django.utils.timezone import now

def mark_attendance_byclass(request, cou_name):
    batch = facultydb.objects.all()
    data = studentdb.objects.filter(c_name=cou_name)
    ctime =datetime.now()
    course_name = cou_name
    batch_name = data[0].b_name
    faculty_name = data[0].s_fac
    teacher_details = {
        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }

    return render(request, "mark_attendence_byclass.html", {
        'data': data,
        'batch': batch,
        'course_name': course_name,
        'batch_name': batch_name,
        'ctime':ctime,
        'faculty_name': faculty_name,'teacher_details':teacher_details
    })



def view_announcementsss(request):
    teacher_name = request.session.get('f_name')  # Assuming f_name is the teacher's name
    ann = notific.objects.filter(facult_name=teacher_name)
    facs=facultydb.objects.all()
    ctime =datetime.now()
    current_date = ctime.strftime("%Y-%m-%d")  # Format YYYY-MM-DD

    # Prepare teacher details from session data
    teacher_details = {

        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }

    # Render the template with filtered announcements
    return render(request, "view_announcements.html", {
        'ctime': ctime,
        'ann': ann,  # Filtered announcements
    'facs':facs,
        'current_date': current_date,
        'teacher_details': teacher_details
    })



def view_announcementsss(request):
    teacher_name = request.session.get('f_name')  # Assuming f_name is the teacher's name
    ann = notific.objects.filter(facult_name=teacher_name)
    facs=facultydb.objects.all()
    ctime =datetime.now()
    current_date = ctime.strftime("%Y-%m-%d")  # Format YYYY-MM-DD

    # Prepare teacher details from session data
    teacher_details = {

        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }

    # Render the template with filtered announcements
    return render(request, "view_announcements.html", {
        'ctime': ctime,
        'ann': ann,  # Filtered announcements
    'facs':facs,
        'current_date': current_date,
        'teacher_details': teacher_details
    })




def save_announcements(req):
    if req.method=="POST":
        a=req.POST.get('notify')
        b=req.POST.get('date')
        c=req.POST.get('fname')

        obj = notific(notificat=a,created=b,facult_name=c)
        obj.save()
        return redirect(view_announcementsss)
def Delete_Announcements(req,an_id):
    x=notific.objects.filter(id=an_id)
    x.delete()
    return redirect(view_announcementsss)



def signin(req):
    return render(req,"signin.html")
def signup(req):
    return render(req,"signup.html")
def signup_signin(req):
    return render(req,"signin.html")
def signup_save(req):
    if req.method == "POST":
        a = req.POST.get('name')
        b = req.POST.get('email')
        c = req.POST.get('pass')
        d = req.POST.get('repass')

        # Check if username or email already exists
        if save_signup.objects.filter(t_name=a).exists():
            messages.warning(req, "Username already exists..!")
            return redirect('signup')  # Assuming you have a 'signup' view to return to
        elif save_signup.objects.filter(t_email=b).exists():
            messages.warning(req, "Email already exists..!")
            return redirect('signup')  # Redirect back to signup if email exists

        # Create new object and save it
        obj = save_signup(t_name=a, t_email=b, t_pass=c, t_repass=d)
        obj.save()
        return redirect('signup')  # Redirect after successful signup

def view_attendence(request):
        today = datetime.today()

        ctime = today.strftime("%d/%m/%Y")
        courses = coursedb.objects.all()
        batch = facultydb.objects.all()
        teacher_details = {
            'f_name': request.session.get('f_name'),
            'f_id': request.session.get('f_id'),
            'course_name': request.session.get('course_name'),
            'batch_name': request.session.get('batch_name'),
            'f_gender': request.session.get('f_gender'),
            'f_dob': request.session.get('f_dob'),
            'f_phn': request.session.get('f_phn'),
            'f_email': request.session.get('f_email'),
            'f_add': request.session.get('f_add'),
            'f_pic': request.session.get('f_pic'),
        }
        return render(request, "view_attendence.html", {'courses': courses, 'ctime': ctime, 'batch': batch,'teacher_details':teacher_details})


def view_attendance_byclass(request, cou_name):
    # Get all batches
    batch = facultydb.objects.all()
    ctime = datetime.now()

    # Filter students based on the course name
    students = studentdb.objects.filter(c_name=cou_name)

    # Check if there are any students for the given course
    if not students.exists():
        return render(request, "view_attendence_byclass.html", {
            'data': students,
            'batch': batch,
            'course_name': cou_name,
            'batch_name': None,
            'faculty_name': None,
            'attendance_stats': {}
        })

    # Get batch name
    batch_name = students[0].b_name

    # Get all faculty members teaching this course (excluding NULL or blank)
    faculty_names = students.values_list('s_fac', flat=True).distinct()


    # Filter attendance records for all faculty
    attendance_records = Attendance.objects.filter(
        course_name__iexact=cou_name,
        batch_name__iexact=batch_name,
        faculty_name__in=faculty_names  # Include all faculty
    )

    # Create a dictionary to hold attendance statistics
    attendance_stats = {}

    # Initialize every student with zero values
    for student in students:
        student_id = student.s_id
        student_name = student.s_name
        attendance_stats[student_id] = {
            'student_name': student_name,
            'total_classes': 0,
            'total_present': 0,
            'total_absent': 0,
            'attendance_percentage': 0,
            'absent_percentage': 0,
        }

    for record in attendance_records:
        student = students.filter(s_id__iexact=record.student_id).first()  # Case-insensitive match
        if student:
            student_id = student.s_id
            if student_id in attendance_stats:
                attendance_stats[student_id]['total_classes'] += 1
                if record.status.lower() == 'present':
                    attendance_stats[student_id]['total_present'] += 1
                elif record.status.lower() == 'absent':
                    attendance_stats[student_id]['total_absent'] += 1

    # Calculate attendance percentage and absent percentage
    for student_id, stats in attendance_stats.items():
        if stats['total_classes'] > 0:
            stats['attendance_percentage'] = round((stats['total_present'] / stats['total_classes']) * 100, 2)
            stats['absent_percentage'] = 100 - stats['attendance_percentage']
        else:
            stats['attendance_percentage'] = 0
            stats['absent_percentage'] = 0  # No classes, no absent percentage

    teacher_details = {
        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }

    return render(request, "view_attendence_byclass.html", {
        'data': students,
        'batch': batch,
        'course_name': cou_name,
        'batch_name': batch_name,
        'faculty_names': faculty_names,  # Display all faculty names
        'attendance_stats': attendance_stats,
        'teacher_details': teacher_details,
        'ctime': ctime,
    })

def dailywisedash(request):
    today = datetime.today()
    ctime = today.strftime("%d/%m/%Y")
    courses = coursedb.objects.all()
    batch = facultydb.objects.all()
    teacher_details = {
        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }
    return render(request,"dailywisedash.html",{'courses': courses, 'ctime': ctime, 'batch': batch,'teacher_details':teacher_details})

from datetime import datetime
from django.shortcuts import render
def view_attendance_bydemo(request, cou_name):
    batch = facultydb.objects.all()
    data = studentdb.objects.filter(c_name=cou_name)
    ctime = datetime.today()

    course_name = cou_name
    batch_name = None
    faculty_name = None

    if data.exists():
        batch_name = data[0].b_name
        faculty_name = data[0].s_fac

    date_filter = request.GET.get('attendance_date', None)

    attendance_records = Attendance.objects.filter(
        course_name=course_name,
        batch_name=batch_name,
        faculty_name=faculty_name,
        status__in=["Present", "Absent"]  # Ensuring valid status
    )

    if date_filter:
        try:
            date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
            attendance_records = attendance_records.filter(attendance_date=date_obj)
        except ValueError:
            pass

    attendance_stats = {}
    for record in attendance_records:
        student_id = record.student_id
        student_name = record.student_name

        if student_id not in attendance_stats:
            attendance_stats[student_id] = {
                'student_name': student_name,
                'status': record.status,
                'total_classes': 0,
                'total_present': 0,
                'total_absent': 0,
            }

        attendance_stats[student_id]['total_classes'] += 1
        if record.status.lower() == 'present':
            attendance_stats[student_id]['total_present'] += 1
        elif record.status.lower() == 'absent':
            attendance_stats[student_id]['total_absent'] += 1

    teacher_details = {
        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }

    return render(request, "view_attendance_bydate.html", {
        'course_name': course_name,
        'batch_name': batch_name,
        'faculty_name': faculty_name,
        'attendance_stats': attendance_stats,
        'date_filter': date_filter,
        'ctime': ctime,
        'teacher_details': teacher_details,
    })

def view_attendance_bydate(request, cou_name):
    # Get all batches
    batch = facultydb.objects.all()
    ctime = datetime.now()

    # Filter students based on the course name
    students = studentdb.objects.filter(c_name=cou_name)

    # Check if there are any students for the given course
    if not students.exists():
        return render(request, "view_attendance_bydate.html", {
            'data': students,
            'batch': batch,
            'course_name': cou_name,
            'batch_name': None,
            'faculty_name': None,
            'attendance_stats': {},
            'ctime': ctime
        })

    # Get batch name and faculty name from the first student
    batch_name = students[0].b_name
    faculty_name = students[0].s_fac

    # Get the date filter from the request (if provided)
    date_filter = request.GET.get('date', None)

    # Filter attendance records based on course name, batch name, faculty name
    attendance_records = Attendance.objects.filter(
        course_name=cou_name,
        batch_name=batch_name,
        faculty_name=faculty_name
    )

    # If a date filter is provided, filter attendance records by date
    if date_filter:
        try:
            date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
            attendance_records = attendance_records.filter(attendance_date=date_obj)
        except ValueError:
            pass  # Handle invalid date format

    # Check if attendance records exist
    if not attendance_records.exists():
        return render(request, "view_attendance_bydate.html", {
            'data': students,
            'batch': batch,
            'course_name': cou_name,
            'batch_name': batch_name,
            'faculty_name': faculty_name,
            'attendance_stats': {},
            'teacher_details': {},
            'ctime': ctime,
            'date_filter': date_filter
        })

    # Create a dictionary to hold attendance statistics
    attendance_stats = {}

    for record in attendance_records:
        student_id = record.student_id
        student_name = record.student_name

        if student_id not in attendance_stats:
            attendance_stats[student_id] = {
                'student_name': student_name,
                'total_classes': 0,
                'total_present': 0,
                'total_absent': 0,
                'attendance_percentage': 0
            }

        attendance_stats[student_id]['total_classes'] += 1

        # Case-insensitive match for status
        status = record.status.lower()
        if status == 'present':
            attendance_stats[student_id]['total_present'] += 1
        elif status == 'absent':
            attendance_stats[student_id]['total_absent'] += 1

    # Calculate attendance percentage
    for student_id, stats in attendance_stats.items():
        if stats['total_classes'] > 0:
            stats['attendance_percentage'] = round((stats['total_present'] / stats['total_classes']) * 100, 2)

    # Get teacher details from session
    teacher_details = {
        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }

    return render(request, "view_attendance_bydate.html", {
        'data': students,
        'batch': batch,
        'course_name': cou_name,
        'batch_name': batch_name,
        'faculty_name': faculty_name,
        'attendance_stats': attendance_stats,
        'teacher_details': teacher_details,
        'ctime': ctime,
        'date_filter': date_filter
    })
def student_leave(request):
    ctime =datetime.now()
    # Get the current teacher's name from the session
    teacher_name = request.session.get('f_name')  # Assuming f_name is the teacher's name

    # Filter student leave records based on the current teacher's name
    std_leave = student_leavedb.objects.filter(l_fname=teacher_name)  # Adjust the field name as necessary

    teacher_details = {
        'f_name': teacher_name,
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }

    return render(request, "student_leave.html", {
        'ctime': ctime,
        'std_leave': std_leave,
        'teacher_details': teacher_details
    })

@csrf_exempt
def check_attendance(request):
    if request.method == 'POST':
        attendance_date = request.POST.get('attendance_date')
        course_name = request.POST.get('course_name')
        batch_name = request.POST.get('batch_name')
        faculty_name = request.POST.get('faculty_name')

        # Check if attendance is already marked for the given date, course, batch, and faculty
        attendance_exists = Attendance.objects.filter(
            attendance_date=attendance_date,
            course_name=course_name,
            batch_name=batch_name,
            faculty_name=faculty_name
        ).exists()

        return JsonResponse({'attendance_exists': attendance_exists})
def student_dashboard(request):
    ctime = datetime.now()

    # Get today's date
    today_date = now().date()

    # Get student details from session
    logged_in_student_name = request.session.get('s_name')
    logged_in_student_email = request.session.get('s_email')
    student_faculty = request.session.get('s_fac')

    # Fetch leave requests for the logged-in student
    leave_requests = student_leavedb.objects.filter(
        l_sname=logged_in_student_name,
        status__in=['Approved', 'Denied']
    ).order_by('-id')  # Sorting by latest first

    # Fetch announcements related to the student's faculty
    ann = notific.objects.filter(facult_name=student_faculty).order_by('-created')

    # Fetch today's attendance notifications for the student's faculty
    today_notifications = Attendance.objects.filter(
        attendance_date=today_date,
        student_name=logged_in_student_name,
        faculty_name=student_faculty  # Only notifications for their faculty
    )

    # Prepare student details dictionary
    student_details = {
        's_name': logged_in_student_name,
        's_id': request.session.get('s_id'),
        's_fac': student_faculty,
        'c_name': request.session.get('c_name'),
        'b_name': request.session.get('b_name'),
        's_gender': request.session.get('s_gender'),
        's_dob': request.session.get('s_dob'),
        's_phn': request.session.get('s_phn'),
        's_email': logged_in_student_email,
        's_add': request.session.get('s_add'),
        'sp_email': request.session.get('sp_email'),
        's_pic': request.session.get('s_pic'),
    }

    # Fetch attendance records for the logged-in student
    atend = Attendance.objects.filter(student_name=logged_in_student_name).order_by('-id')  # Latest first

    # Prepare attendance events for the calendar
    events = []
    for record in atend:
        color = 'green' if record.status == 'present' else 'red' if record.status == 'absent' else 'gray'
        events.append({
            'title': record.status,
            'start': record.attendance_date.strftime('%Y-%m-%d'),
            'backgroundColor': color,
            'borderColor': color,
            'textColor': 'white',
        })

    # Debugging: Print the notifications to check if they're being fetched

    return render(request, "student_dashboard.html", {
        'ctime': ctime,
        'student_details': student_details,
        'leave_requests': leave_requests,
        'ann': ann,
        'atend': atend,
        'events': events,
        'today_notifications': today_notifications  # Pass to template
    })



def Add_Student_Leaves(request):
    ctime = datetime.now()
    student_details = {
        's_name': request.session.get('s_name'),
        's_id': request.session.get('s_id'),
        's_fac': request.session.get('s_fac'),
        'c_name': request.session.get('c_name'),
        'b_name': request.session.get('b_name'),
        's_gender': request.session.get('s_gender'),
        's_dob': request.session.get('s_dob'),
        's_phn': request.session.get('s_phn'),
        's_email': request.session.get('s_email'),
        's_add': request.session.get('s_add'),
        'sp_email': request.session.get('sp_email'),
        's_pic': request.session.get('s_pic'),
    }
    return render(request,"Add_Student_Leaves.html",{'student_details':student_details,'ctime':ctime})


def student_signin(req):
    return render(req,"student_signin.html")


def signup_savestudent(req):
    if req.method=="POST":
        a=req.POST.get('name')
        b=req.POST.get('email')
        c=req.POST.get('pass')
        d=req.POST.get('repass')
        obj=studnt_signup(studnt_name=a,studnt_email=b,studnt_pass=c,studnt_repass=d)
        if studnt_signup.objects.filter(studnt_name=a).exists():
            messages.warning(req, "Name already exists..!")
            return redirect(signup)
        elif studnt_signup.objects.filter(studnt_email=b).exists():
            messages.warning(req, "Email already exists..!")
            return redirect(signup)
        obj.save()
        return redirect(signup)


def signin_student(request):
    if request.method == "POST":
        username = request.POST.get('user')  # This is the username (or student ID)
        password = request.POST.get('pass')   # This is the password

        # Authenticate the user
        try:
            # Fetch the user record based on the provided username
            user = studnt_signup.objects.get(studnt_name=username)
            if user.studnt_pass == password:  # In production, use hashed password comparison
                # Fetch student details from the studentdb model
                student = studentdb.objects.get(s_name=username)  # Assuming s_id is the same as username

                # Store student details in the session
                request.session['s_name'] = student.s_name
                request.session['s_id'] = student.s_id
                request.session['s_fac'] = student.s_fac
                request.session['c_name'] = student.c_name
                request.session['b_name'] = student.b_name
                request.session['s_gender'] = student.s_gender
                request.session['s_dob'] = student.s_dob
                request.session['s_phn'] = student.s_phn
                request.session['s_email'] = student.s_email
                request.session['s_add'] = student.s_add
                request.session['sp_email'] = student.sp_email
                request.session['s_pic'] = student.s_pic.url if student.s_pic else None  # Get the URL of the image

                messages.success(request, "Login Successfully to AMS Student Dashboard..!")
                return redirect(student_dashboard)  # Redirect to the student dashboard
            else:
                messages.warning(request, "Invalid Password")
                return redirect('signin')  # Redirect back to the login page
        except studnt_signup.DoesNotExist:
            messages.warning(request, "Invalid Username")
            return redirect('signin')  # Redirect back to the login page
        except studentdb.DoesNotExist:
            messages.warning(request, "Student details not found.")
            return redirect('signin')  # Redirect back to the login page
    else:
        return redirect('signin')  # Redirect to the login page for GET requests
def signin_op(request):
    if request.method == "POST":
        username = request.POST.get('user')  # This is the username (or student ID)
        password = request.POST.get('pass')   # This is the password

        # Authenticate the user
        try:
            # Fetch the user record based on the provided username
            user = save_signup.objects.get(t_name=username)
            if user.t_pass == password:  # In production, use hashed password comparison
                # Fetch student details from the studentdb model
                teacher = facultydb.objects.get(f_name=username)  # Assuming s_id is the same as username

                # Store student details in the session
                request.session['f_name'] = teacher.f_name
                request.session['f_id'] = teacher.f_id
                request.session['course_name'] = teacher.course_name
                request.session['batch_name'] = teacher.batch_name
                request.session['f_gender'] = teacher.f_gender
                request.session['f_dob'] = teacher.f_dob
                request.session['f_phn'] = teacher.f_phn
                request.session['f_email'] = teacher.f_email
                request.session['f_add'] = teacher.f_add
                request.session['f_pic'] = teacher.f_pic.url if teacher.f_pic else None  # Get the URL of the image

                messages.success(request, "Login Successfully to AMS Teacher Dashboard..!")
                return redirect(home)  # Redirect to the student dashboard
            else:
                messages.warning(request, "Invalid Password")
                return redirect('signin')  # Redirect back to the login page
        except save_signup.DoesNotExist:
            messages.warning(request, "Invalid Username")
            return redirect('signin')  # Redirect back to the login page
        except facultydb.DoesNotExist:
            messages.warning(request, "Teacher details not found.")
            return redirect('signin')  # Redirect back to the login page
    else:
        return redirect('signin')  # Redirect to the login page for GET requests










def profile_teacher(request):
    teacher_details = {
        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }
    return render(request,"profile_teacher.html",{'teacher_details':teacher_details})



def profile_student(request):
    student_details = {
        's_name': request.session.get('s_name'),
        's_id': request.session.get('s_id'),
        's_fac': request.session.get('s_fac'),
        'c_name': request.session.get('c_name'),
        'b_name': request.session.get('b_name'),
        's_gender': request.session.get('s_gender'),
        's_dob': request.session.get('s_dob'),
        's_phn': request.session.get('s_phn'),
        's_email': request.session.get('s_email'),
        's_add': request.session.get('s_add'),
        'sp_email': request.session.get('sp_email'),
        's_pic': request.session.get('s_pic'),
    }
    return render(request,"demo.html",{'student_details':student_details})


def save_student_leaves(req):
    if req.method=="POST":
        a=req.POST.get('lsname')
        b=req.POST.get('lcname')
        c=req.POST.get('lfname')
        d=req.POST.get('date')
        e=req.POST.get('lreason')
        obj = student_leavedb(l_sname=a,l_cname=b,l_fname=c,l_ndate=d,l_reason=e)
        obj.save()
        return redirect(Add_Student_Leaves)



@csrf_exempt  # Use this if you are not using CSRF tokens in AJAX requests
def update_leave_status(request):
    if request.method == 'POST':
        leave_id = request.POST.get('leave_id')
        status = request.POST.get('status')

        try:
            leave_request = student_leavedb.objects.get(id=leave_id)
            leave_request.status = status
            leave_request.save()
            return JsonResponse({'success': True, 'status': status})
        except student_leavedb.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Leave request not found.'})

    return JsonResponse({'success': False, 'error': 'Invalid request.'})


from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

def render_to_pdf(template_path, context={}):
    """
    This function converts a Django
     template to a PDF.
    """
    # Get the HTML template
    template = get_template(template_path)
    html = template.render(context)

    # Create a BytesIO object to store the PDF content
    pdf = BytesIO()

    # Use xhtml2pdf to generate the PDF
    pisa_status = pisa.CreatePDF(html, dest=pdf)

    # If there is an error, return None
    if pisa_status.err:
        return None

    # Reset the buffer pointer to the beginning
    pdf.seek(0)

    # Return the generated PDF as an HTTP response
    response = HttpResponse(pdf.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="document.pdf"'

    return response



def generate_attendance_pdf(request, course_name, batch_name):
    # Fetch attendance records for the given course and batch
    attendance_records = Attendance.objects.filter(course_name=course_name, batch_name=batch_name)
    attendance_stats = {}
    if attendance_records.exists():
        faculty_name = attendance_records.first().faculty_name  # Get faculty name from the first record
    else:
        faculty_name = 'Unknown Faculty'  # Default value if no records found
    for record in attendance_records:
        status_normalized = record.status.strip().lower()  # Normalize: Remove spaces & lowercase

        student_id = record.student_id
        student_name = record.student_name

        if student_id not in attendance_stats:
            attendance_stats[student_id] = {
                'student_name': student_name,
                'total_classes': 0,
                'total_present': 0,
                'total_absent': 0,
            }

        attendance_stats[student_id]['total_classes'] += 1

        if status_normalized in ['present', 'prsent']:  # Handle both variations
            attendance_stats[student_id]['total_present'] += 1
        elif status_normalized == 'absent':
            attendance_stats[student_id]['total_absent'] += 1

    # Calculate attendance percentage
    for student_id, stats in attendance_stats.items():
        if stats['total_classes'] > 0:
            stats['attendance_percentage'] = (stats['total_present'] / stats['total_classes']) * 100
        else:
            stats['attendance_percentage'] = 0

    context = {
        'course_name': course_name,
        'batch_name': batch_name,
        'faculty_name': faculty_name,  # Replace with actual faculty name
        'attendance_stats': attendance_stats,
        'ctime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Call the render_to_pdf function to generate the PDF
    return render_to_pdf('view_attendance_by_classpdf.html', context)






def course_filterpdf(request, cou_name):
    """
    Fetches student data filtered by course name and allows users to download it as a PDF.
    """
    ctime =datetime.now()
    data = studentdb.objects.filter(c_name=cou_name)  # Filter students by course name

    # Ensure there is at least one student to prevent errors
    batch_name = data[0].b_name if data else "Unknown"
    faculty_name = data[0].s_fac if data else "Unknown"

    # Fetch teacher details from session (optional)
    teacher_details = {
        'f_name': request.session.get('f_name', "Unknown"),
        'f_id': request.session.get('f_id', "Unknown"),
        'course_name': request.session.get('course_name', cou_name),
        'batch_name': request.session.get('batch_name', batch_name),
        'f_gender': request.session.get('f_gender', "Unknown"),
        'f_dob': request.session.get('f_dob', "Unknown"),
        'f_phn': request.session.get('f_phn', "Unknown"),
        'f_email': request.session.get('f_email', "Unknown"),
        'f_add': request.session.get('f_add', "Unknown"),
        'f_pic': request.session.get('f_pic', ""),
    }

    context = {
        'data': data,
        'course_name': cou_name,
        'batch_name': batch_name,
        'faculty_name': faculty_name,
        'teacher_details': teacher_details,
        'ctime': ctime,
    }

    # Check if the user wants to download the PDF
    if request.GET.get('download_pdf'):
        return render_to_pdf2("view_class_pdf.html", context, course_name=cou_name)  # Generate the PDF

    # Otherwise, render the regular webpage
    return render(request, "view_class.html", context)

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

def render_to_pdf2(template_path, context={}, course_name="document"):
    """
    Converts a Django template to a downloadable PDF file.
    """
    template = get_template(template_path)
    html = template.render(context)

    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf)

    if pisa_status.err:
        return None

    pdf.seek(0)

    # Generate the filename dynamically
    safe_course_name = course_name.replace(" ", "_")
    filename = f"Class_details_of_{safe_course_name}.pdf"

    response = HttpResponse(pdf.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


def render_to_pdf_attendancebydemo(template_path, context, filename="document"):
    """
    Converts a Django template into a PDF and returns it as an HTTP response.
    """
    template = get_template(template_path)
    html = template.render(context)
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf)

    if pisa_status.err:
        return None

    pdf.seek(0)
    response = HttpResponse(pdf.read(), content_type='application/pdf')

    # Set dynamically generated filename
    safe_filename = filename.replace(" ", "_")  # Replace spaces with underscores
    response['Content-Disposition'] = f'attachment; filename="{safe_filename}.pdf"'

    return response


def view_attendance_bydemopdf(request, cou_name):
    # Fetch batch and student data for the given course
    batch = facultydb.objects.all()
    data = studentdb.objects.filter(c_name=cou_name)
    ctime =datetime.now()

    # Handle missing data gracefully
    course_name = cou_name
    batch_name = data[0].b_name if data else "Unknown"
    faculty_name = data[0].s_fac if data else "Unknown"

    # Get attendance date filter from GET request
    date_filter = request.GET.get('attendance_date', None)
    attendance_records = Attendance.objects.filter(course_name=course_name, batch_name=batch_name,
                                                   faculty_name=faculty_name)

    # Filter attendance records by date if provided
    if date_filter:
        try:
            date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
            attendance_records = attendance_records.filter(attendance_date=date_obj)
        except ValueError:
            pass  # Handle invalid date format

    # Prepare attendance statistics
    attendance_stats = {}
    for record in attendance_records:
        student_id = record.student_id
        student_name = record.student_name
        attendance_stats[student_id] = {
            'student_name': student_name,
            'status': record.status,  # 'Present' or 'Absent'
        }

    # Fetch teacher details from session (with fallback if necessary)
    teacher_details = {
        'f_name': request.session.get('f_name', 'N/A'),
        'f_id': request.session.get('f_id', 'N/A'),
        'course_name': request.session.get('course_name', course_name),
        'batch_name': request.session.get('batch_name', batch_name),
        'f_gender': request.session.get('f_gender', 'N/A'),
        'f_dob': request.session.get('f_dob', 'N/A'),
        'f_phn': request.session.get('f_phn', 'N/A'),
        'f_email': request.session.get('f_email', 'N/A'),
        'f_add': request.session.get('f_add', 'N/A'),
        'f_pic': request.session.get('f_pic', 'N/A'),
    }

    # If the user requests a PDF download
    if request.GET.get('download_pdf'):
        context = {
            'course_name': course_name,
            'batch_name': batch_name,
            'faculty_name': faculty_name,
            'attendance_stats': attendance_stats,
            'date_filter': date_filter,
            'ctime': ctime,
            'teacher_details': teacher_details,
        }

        # Generate filename dynamically based on the selected date filter
        selected_date = date_filter if date_filter else "All_Dates"
        filename = f"Attendance_Report_of_{course_name}_on_{selected_date}"

        # Call your function to generate the PDF
        return render_to_pdf_attendancebydemo('view_attendance_bydemopdf.html', context, filename=filename)

    # Otherwise, render the normal HTML page
    return render(request, "view_attendance_bydate.html", {
        'course_name': course_name,
        'batch_name': batch_name,
        'faculty_name': faculty_name,
        'attendance_stats': attendance_stats,
        'date_filter': date_filter,
        'ctime': ctime,
        'teacher_details': teacher_details,
    })

def edit_view_attendence(request):
    today = datetime.today()
    ctime = today.strftime("%d/%m/%Y")
    courses = coursedb.objects.all()
    batch = facultydb.objects.all()
    teacher_details = {
        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
        }
    return render(request, "edit_view_attendance.html",
                      {'courses': courses, 'ctime': ctime, 'batch': batch, 'teacher_details': teacher_details})


def delete_students(req,ss_id):
    x=studentdb.objects.filter(id=ss_id)
    x.delete()
    return redirect(view_students)

from django.contrib.auth import logout
def logout_view(request):
    logout(request)  # This will clear the session
    return redirect(signin)

def logout_view_stud(request):
    logout(request)  # This will clear the session
    return redirect(signin)



def calendar_view(request):
    from django.utils import timezone

    student_details = {
        's_name':request.session.get('s_name'),
        's_id': request.session.get('s_id'),
        's_fac': request.session.get('s_fac'),
        'c_name': request.session.get('c_name'),
        'b_name': request.session.get('b_name'),
        's_gender': request.session.get('s_gender'),
        's_dob': request.session.get('s_dob'),
        's_phn': request.session.get('s_phn'),
        's_email': request.session.get('s_email'),
        's_add': request.session.get('s_add'),
        'sp_email': request.session.get('sp_email'),
        's_pic': request.session.get('s_pic'),
    }
    stud_name = request.session.get('s_name')


def calendar_view(request):
    student_details = {
        's_name': request.session.get('s_name'),
        's_id': request.session.get('s_id'),
        's_fac': request.session.get('s_fac'),
        'c_name': request.session.get('c_name'),
        'b_name': request.session.get('b_name'),
        's_gender': request.session.get('s_gender'),
        's_dob': request.session.get('s_dob'),
        's_phn': request.session.get('s_phn'),
        's_email': request.session.get('s_email'),
        's_add': request.session.get('s_add'),
        'sp_email': request.session.get('sp_email'),
        's_pic': request.session.get('s_pic'),
    }

    stud_name = request.session.get('s_name')

    # Fetch attendance records for the logged-in student
    atend = Attendance.objects.filter(student_name=stud_name).order_by('-id')  # Sorting by latest first

    # Calculate attendance percentage
    total_classes = atend.count()
    present_count = atend.filter(status__iexact='present').count()  # Case-insensitive match for 'present'

    attendance_percentage = round((present_count / total_classes) * 100, 2) if total_classes > 0 else 0

    events = []
    for record in atend:
        if record.status.lower() == 'present':
            color = 'green'
        elif record.status.lower() == 'absent':
            color = 'red'
        else:
            color = 'gray'

        events.append({
            'title': record.status,
            'start': record.attendance_date.strftime('%Y-%m-%d'),
            'backgroundColor': color,
            'borderColor': color,
            'textColor': 'white',
        })

    return render(request, "calendr_template.html", {
        'student_details': student_details,
        'atend': atend,
        'events': events,  # Pass events to the template
        'attendance_percentage': attendance_percentage  # Pass attendance percentage
    })


def attendance_email(request, cou_name):
    import datetime
    batch = facultydb.objects.all()
    ctime = datetime.datetime.now()

    # Get students enrolled in the given course
    students = studentdb.objects.filter(c_name=cou_name)

    # If no students exist for the given course, return empty stats
    if not students.exists():
        return render(request, "attendance_email.html", {
            'data': students,
            'batch': batch,
            'course_name': cou_name,
            'batch_name': None,
            'faculty_name': None,
            'attendance_stats': {}
        })

    # Get batch name
    batch_name = students[0].b_name

    # Get all faculty members teaching this course (exclude NULL and blank values)
    faculty_names = students.exclude(s_fac__isnull=True).exclude(s_fac="").values_list('s_fac', flat=True).distinct()
    faculty_names = list(map(str.strip, faculty_names))  # Remove extra spaces

    # Filter attendance records for all faculties of this course
    attendance_records = Attendance.objects.filter(
        course_name__iexact=cou_name,
        batch_name__iexact=batch_name,
        faculty_name__in=faculty_names
    )

    # Dictionary to store attendance statistics
    attendance_stats = {}

    # Initialize all students in attendance_stats
    for student in students:
        student_id = student.s_id
        student_name = student.s_name
        parent_email = student.sp_email  # Fetch parent's email from studentdb

        attendance_stats[student_id] = {
            'student_name': student_name,
            'parent_email': parent_email,
            'total_classes': 0,
            'total_present': 0,
            'total_absent': 0,
            'attendance_percentage': 0,
            'absent_percentage': 0,
        }

    # Update attendance statistics based on records
    for record in attendance_records:
        student = students.filter(s_name__iexact=record.student_name).first()  # Case-insensitive match
        if student:
            student_id = student.s_id
            if student_id in attendance_stats:
                attendance_stats[student_id]['total_classes'] += 1
                if record.status.lower() == 'present':
                    attendance_stats[student_id]['total_present'] += 1
                elif record.status.lower() == 'absent':
                    attendance_stats[student_id]['total_absent'] += 1

    # Calculate attendance percentage and filter students below 75%
    filtered_attendance_stats = {}
    for student_id, stats in attendance_stats.items():
        if stats['total_classes'] > 0:
            stats['attendance_percentage'] = round((stats['total_present'] / stats['total_classes']) * 100, 2)
            stats['absent_percentage'] = 100 - stats['attendance_percentage']
        else:
            stats['attendance_percentage'] = 0
            stats['absent_percentage'] = 0

        if stats['attendance_percentage'] < 75:
            filtered_attendance_stats[student_id] = stats

    # Teacher details
    teacher_details = {
        'f_name': request.session.get('f_name'),
        'f_id': request.session.get('f_id'),
        'course_name': request.session.get('course_name'),
        'batch_name': request.session.get('batch_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_email': request.session.get('f_email'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }

    return render(request, "attendance_email.html", {
        'data': students,
        'batch': batch,
        'course_name': cou_name,
        'batch_name': batch_name,
        'faculty_names': faculty_names,  # Display all faculty names
        'attendance_stats': filtered_attendance_stats,  # Only students <75% attendance
        'teacher_details': teacher_details,
        'ctime': ctime,
    })

from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages

def send_attendance_email(request):
    if request.method == "POST":
        student_name = request.POST.get("student_name")
        parent_email = request.POST.get("parent_email")
        faculty_name=request.POST.get("faculty_name")
        attendance_percentage = request.POST.get("attendance_percentage")

        if not parent_email:
            messages.error(request, "Parent email is missing.")
            return redirect(dailywisedash)  # Redirect back to attendance page

        # Email Content
        subject = f"Low Attendance Alert for {student_name}"
        message = (
            f"Dear Parent,\n\n"
            f"I am writing to inform you that {student_name}'s current attendance rate is {attendance_percentage} %. "
            f"Please ensure they attend classes regularly to avoid issues.\n\n"
            f"Best regards,\n"
            f"AMS Administration"
        )

        # Send the email
        send_mail(
            subject,
            message,
            "merlyndeena@gmail.com",  # Sender Email (Change this to your actual email)
            [parent_email],  # Recipient Email
            fail_silently=False,
        )

        # Show Success Message
        messages.success(request, f"Email sent successfully to {parent_email}.")

        return redirect(dailywisedash)  # Redirect back to the attendance page

    return JsonResponse({"error": "Invalid request"}, status=400)






def batch_attendance(request):
        # Get the logged-in faculty name from the session
        faculty_name = request.session.get('f_name')
        batch_name=request.session.get('b_name')
        course_name= request.session.get('course_name')

        # If no faculty is logged in, show an error
        if not faculty_name:
            return render(request, "faculty_attendance.html", {
                'error': "Faculty not logged in.",
                'attendance_stats': {}
            })

        # Get the current date
        today_date = now().date()

        # Filter students based on the logged-in faculty
        students = studentdb.objects.filter(s_fac=faculty_name)

        # If no students exist under this faculty, return an error message
        if not students.exists():
            return render(request, "faculty_attendance.html", {
                'error': "No students found under this faculty.",
                'attendance_stats': {}
            })

        # Extract student IDs to use for attendance filtering
        student_ids = students.values_list('s_id', flat=True)

        # Fetch attendance records only for the filtered students
        attendance_records = Attendance.objects.filter(student_id__in=student_ids)

        # Create a dictionary to store attendance statistics
        attendance_stats = {}

        # Initialize each student's record with zero values
        for student in students:
            student_id = student.s_id
            student_name = student.s_name

            attendance_stats[student_id] = {
                'student_name': student_name,
                'total_classes': 0,
                'total_present': 0,
                'total_absent': 0,
                'attendance_percentage': 0,
                'absent_percentage': 0,
            }

        # Process attendance records and count present/absent days
        for record in attendance_records:
            student_id = record.student_id
            if student_id in attendance_stats:
                attendance_stats[student_id]['total_classes'] += 1
                if record.status.lower() in ['present', 'prsent']:  # Handles common typo
                    attendance_stats[student_id]['total_present'] += 1
                elif record.status.lower() == 'absent':
                    attendance_stats[student_id]['total_absent'] += 1

        # Calculate attendance percentage
        for student_id, stats in attendance_stats.items():
            if stats['total_classes'] > 0:
                stats['attendance_percentage'] = round((stats['total_present'] / stats['total_classes']) * 100, 2)
                stats['absent_percentage'] = 100 - stats['attendance_percentage']
            else:
                stats['attendance_percentage'] = 0
                stats['absent_percentage'] = 0

        # Fetch faculty details from session
        teacher_details = {
            'f_name': faculty_name,
            'f_id': request.session.get('f_id'),
            'course_name': request.session.get('course_name'),
            'batch_name': request.session.get('batch_name'),
            'f_gender': request.session.get('f_gender'),
            'f_dob': request.session.get('f_dob'),
            'f_phn': request.session.get('f_phn'),
            'f_email': request.session.get('f_email'),
            'f_add': request.session.get('f_add'),
            'f_pic': request.session.get('f_pic'),
        }

        return render(request, "batch_attendance.html", {
            'attendance_stats': attendance_stats,
            'teacher_details': teacher_details,
            'today_date': today_date,
            'course_name':course_name,
            'batch_name':batch_name,
            'faculty_name':faculty_name

        })

def low_Attendance(request):
    ctime = now()
    today_date = ctime.date()

    # Get logged-in teacher's details
    faculty_name = request.session.get('f_name')


    if not faculty_name:
        return render(request, "attendance_email.html", {
            'error': "You need to log in as a faculty member.",
            'attendance_stats': {},
            'ctime': ctime,
        })

    # Fetch students assigned to the logged-in faculty
    students = studentdb.objects.filter(s_fac=faculty_name)

    if not students.exists():
        return render(request, "attendance_email.html", {
            'error': "No students found under your supervision.",
            'attendance_stats': {},
            'ctime': ctime,
        })

    batch_name = students.first().b_name  # Assuming all students belong to the same batch

    # Filter attendance records for this faculty's students
    attendance_records = Attendance.objects.filter(
        faculty_name=faculty_name,
        batch_name=batch_name,
    )

    # Dictionary to store attendance statistics
    attendance_stats = {}

    for student in students:
        student_id = student.s_id
        student_name = student.s_name
        parent_email = student.sp_email  # Parent's email

        attendance_stats[student_id] = {
            'student_name': student_name,
            'parent_email': parent_email,
            'total_classes': 0,
            'total_present': 0,
            'total_absent': 0,
            'attendance_percentage': 0,
            'absent_percentage': 0,  # Initialize absent percentage
        }

    # Update attendance records
    for record in attendance_records:
        student = students.filter(s_id=record.student_id).first()
        if student:
            student_id = student.s_id
            if student_id in attendance_stats:
                attendance_stats[student_id]['total_classes'] += 1
                if record.status.lower() in ['present', 'prsent']:  # Handling case variations
                    attendance_stats[student_id]['total_present'] += 1
                elif record.status.lower() == 'absent':
                    attendance_stats[student_id]['total_absent'] += 1

    # Calculate attendance percentage & filter students <75%
    filtered_attendance_stats = {}
    for student_id, stats in attendance_stats.items():
        if stats['total_classes'] > 0:
            stats['attendance_percentage'] = round((stats['total_present'] / stats['total_classes']) * 100, 2)
            stats['absent_percentage'] = round(100 - stats['attendance_percentage'], 2)  # Calculate absent percentage
        else:
            stats['attendance_percentage'] = 0
            stats['absent_percentage'] = 100  # If no classes, assume 100% absent

        if stats['attendance_percentage'] < 75:
            filtered_attendance_stats[student_id] = stats  # Only students <75%

    teacher_details = {
        'f_name': faculty_name,
        'f_id': request.session.get('f_id'),
        'batch_name': request.session.get('batch_name'),
        'f_email': request.session.get('f_email'),
        'course_name': request.session.get('course_name'),
        'f_gender': request.session.get('f_gender'),
        'f_dob': request.session.get('f_dob'),
        'f_phn': request.session.get('f_phn'),
        'f_add': request.session.get('f_add'),
        'f_pic': request.session.get('f_pic'),
    }

    return render(request, "low_attendance.html", {
        'attendance_stats': filtered_attendance_stats,
        'teacher_details': teacher_details,
        'ctime': ctime,
    })

