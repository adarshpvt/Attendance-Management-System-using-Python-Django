from django.db import models





class coursedb(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    bname = models.CharField(max_length=255,null=True,blank=True)



class facultydb(models.Model):
    f_name = models.CharField(max_length=100, null=True, blank=True)
    f_id = models.CharField(max_length=100, null=True, blank=True)
    course_name = models.CharField(max_length=100, null=True, blank=True)
    batch_name = models.CharField(max_length=100, null=True, blank=True)
    f_gender = models.CharField(max_length=100, null=True, blank=True)
    f_dob = models.CharField(max_length=100, null=True, blank=True)
    f_phn = models.CharField(max_length=100, null=True, blank=True)
    f_email = models.EmailField(max_length=100, null=True, blank=True)
    f_add = models.TextField(max_length=100, null=True, blank=True)
    f_pic = models.ImageField(upload_to="Faculty_Images", null=True, blank=True)
class studentdb(models.Model):
    s_name = models.CharField(max_length=100, null=True, blank=True)
    s_id = models.CharField(max_length=100, null=True, blank=True)
    s_fac = models.CharField(max_length=100, null=True, blank=True)
    c_name = models.CharField(max_length=100, null=True, blank=True)
    b_name = models.CharField(max_length=100, null=True, blank=True)
    s_gender = models.CharField(max_length=100, null=True, blank=True)
    s_dob = models.CharField(max_length=100, null=True, blank=True)
    s_phn = models.CharField(max_length=100, null=True, blank=True)
    s_email = models.EmailField(max_length=100, null=True, blank=True)
    s_add = models.TextField(max_length=100, null=True, blank=True)
    sp_email = models.EmailField(max_length=100, null=True, blank=True)
    s_pic = models.ImageField(upload_to="Student_Images", null=True, blank=True)
class notific(models.Model):
    notificat=models.CharField(max_length=100,null=True,blank=True)
    created=models.CharField(max_length=100,null=True)
    facult_name=models.CharField(max_length=100,null=True,blank=True)








