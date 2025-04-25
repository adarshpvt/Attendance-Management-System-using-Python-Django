from django.db import models






class save_signup(models.Model):
    t_name=models.CharField(max_length=100,null=True,blank=True)
    t_email=models.CharField(max_length=100,null=True,blank=True)
    t_pass=models.CharField(max_length=100,null=True,blank=True)
    t_repass=models.CharField(max_length=100,null=True,blank=True)




class Attendance(models.Model):
    course_name = models.CharField(max_length=100,null=True)  # Name of the course
    batch_name = models.CharField(max_length=100,null=True)   # Name of the batch
    faculty_name = models.CharField(max_length=100,null=True)  # Name of the faculty
    attendance_date = models.DateField(null=True)             # Date of attendance
    student_id = models.CharField(max_length=50,null=True)
    student_name = models.CharField(max_length=50,null=True)
    # Unique ID of the student
    status = models.CharField(max_length=10,null=True)         # Attendance status ('present' or 'absent')

    def __str__(self):
        return f"{self.student_id} - {self.status} on {self.attendance_date}"


class studnt_signup(models.Model):
    studnt_name=models.CharField(max_length=100,null=True,blank=True)
    studnt_email=models.CharField(max_length=100,null=True,blank=True)
    studnt_pass=models.CharField(max_length=100,null=True,blank=True)
    studnt_repass=models.CharField(max_length=100,null=True,blank=True)


class student_leavedb(models.Model):
    l_sname=models.CharField(max_length=100,null=True,blank=True)
    l_cname=models.CharField(max_length=100,null=True,blank=True)
    l_fname=models.CharField(max_length=100,null=True,blank=True)
    l_ndate=models.CharField(max_length=100,null=True,blank=True)
    l_reason=models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(max_length=10,
                              choices=[('Approved', 'Approved'), ('Denied', 'Denied'), ('Pending', 'Pending')],
                              default='Pending')

