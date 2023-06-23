from django import forms
from django.forms import ModelForm
from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(UserCreationForm):
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}))
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email','phone','address','password','is_superuser']
        # fields = '__all__'

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def clean_name(self):
        if len(self.cleaned_data['name']) > 10:
            print(len(self.cleaned_data['name']))
            raise ValidationError("Course Name is too lengthy")
        return self.cleaned_data['name']