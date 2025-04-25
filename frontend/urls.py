from django.urls import path
from frontend import views
urlpatterns=[
    path('home/',views.home,name="home"),
    path('student/',views.student,name="student"),


    path('fac/',views.fac,name="fac"),
    path('save_Tstudent/',views.save_Tstudent,name="save_Tstudent"),
    path('view_students/',views.view_students,name="view_students"),

    path('editstudents/<int:s_id>/', views.editstudents, name="editstudents"),
    path('signin/', views.signin, name="signin"),


    path('view_batches/', views.view_batches, name="view_batches"),
    path('course_filter/<cou_name>/', views.course_filter, name="course_filter"),


    path('signup/', views.signup, name="signup"),
    path('', views.signin, name="signin"),
    path('signup_signin', views.signup_signin, name="signup_signin"),
    path('signup_save/', views.signup_save, name="signup_save"),
    path('signin_op/', views.signin_op, name="signin_op"),

    path('mark_attendance/',views.mark_attendance,name="mark_attendance"),
    path('save_attendance/', views.save_attendance, name="save_attendance"),
    path('mark_attendance_byclass/<cou_name>/', views.mark_attendance_byclass, name="mark_attendance_byclass"),


    path('dailywisedash/', views.dailywisedash, name="dailywisedash"),
    path('view_attendance_bydate/<cou_name>', views.view_attendance_bydate, name="view_attendance_bydate"),

    path('view_attendence/', views.view_attendence, name="view_attendence"),
    path('view_attendance_byclass/<cou_name>/', views.view_attendance_byclass, name="view_attendance_byclass"),
    path('view_attendance_bydemo/<cou_name>/', views.view_attendance_bydemo, name="view_attendance_bydemo"),


    path('view_announcementsss/', views.view_announcementsss, name="view_announcementsss"),
    path('save_announcements/', views.save_announcements, name="save_announcements"),
    path('Delete_Announcements/<int:an_id>/', views.Delete_Announcements, name="Delete_Announcements"),

    path('student_leave/', views.student_leave, name="student_leave"),
    path('save_student_leaves/', views.save_student_leaves, name="save_student_leaves"),




    path('student_dashboard/', views.student_dashboard, name="student_dashboard"),
    path('Add_Student_Leaves/', views.Add_Student_Leaves, name="Add_Student_Leaves"),

    path('signin_student/', views.signin_student, name="signin_student"),
    path('signup_savestudent/', views.signup_savestudent, name="signup_savestudent"),

    path('profile_student/', views.profile_student, name="profile_student"),
    path('profile_teacher/', views.profile_teacher, name="profile_teacher"),
    path('edit_view_attendence/', views.edit_view_attendence, name="edit_view_attendence"),

    path('update_leave_status/',views.update_leave_status, name='update_leave_status'),
    path('logout_view/',views.logout_view, name='logout_view'),
    path('logout_view_stud/',views.logout_view_stud, name='logout_view_stud'),
    path('attendance/pdf/<str:course_name>/<str:batch_name>/', views.generate_attendance_pdf, name='generate_attendance_pdf'),
    path('course_filterpdf/<str:cou_name>/', views.course_filterpdf, name='course_filterpdf'),

    path('view_attendance_bydemopdf/<str:cou_name>/',views.view_attendance_bydemopdf, name='view_attendance_bydemopdf'),
    path('delete_students/<int:ss_id>/',views.delete_students, name='delete_students'),
    path('calendar_view/', views.calendar_view, name='calendar_view'),
    path('attendance_email/<cou_name>', views.attendance_email, name='attendance_email'),
    path('check_attendance/', views.check_attendance, name='check_attendance'),
    path("send_attendance_email/",views.send_attendance_email, name="send_attendance_email"),
    path("batch_attendance/",views.batch_attendance, name="batch_attendance"),
    path("low_Attendance/",views.low_Attendance, name="low_Attendance"),

]