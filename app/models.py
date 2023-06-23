from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.template.defaultfilters import slugify
# from autoslug import AutoSlugField

# Create your models here.

CHOICE_TAG = (
    ('student','student'),
    ('staff','staff'),
    ('hod','hod')
)
STD_CHOCE = {
    ('9','9'),
    ('10','10'),
    ('11','11'),
    ('12','12')

}





class CustomUser(AbstractUser):
    phone = models.CharField(max_length=12)
    address = models.TextField(max_length=200)

    def __str__(self):
        return self.username    

class Course(models.Model):
    name = models.CharField(max_length=100)
  
    def __str__(self):
        return self.name    
        
class Student(models.Model):
    related_course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True)
    name = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='cust_user')
    roll_no = models.IntegerField() 
    user_tag = models.CharField(choices=CHOICE_TAG, default = 'student', max_length=50)
    std = models.CharField(choices=STD_CHOCE, default= '10', max_length=50)
    # class Meta:
    #     unique_together = ["roll_no", "std"]
        # constraints = [
        #     models.UniqueConstraint(fields=['roll_no','std'],name="Unique identity")
        # ]

    class Meta:
        verbose_name_plural = "All Students"    
        # ordering = ('std',)
    def __str__(self):
        return self.name.username 

    

class Subject(models.Model):
    name = models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default="NOTHING")
    def __str__(self):
        return self.name

class Staff(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='CustomUserStaff')
    user_tag = models.CharField(choices=CHOICE_TAG, default = '2', max_length=50)  
    subject = models.ForeignKey(Subject,on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.user.username + "  " + self.user_tag











