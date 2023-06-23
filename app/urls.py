
from django.contrib import admin
from django.urls import path,include
from .views import *
from .ser_view import *
from app import views
from django.contrib import admin
from django.urls import path,include
from .views import *

from app import views
from rest_framework import routers
urlpatterns = [
    path('UserLogin/',views.UserLogin, name="UserLogin"),
    path('home/',views.home, name="home"),
    path('RegisterUser/',views.RegisterUser,name="RegisterUser"),
    path('userLogout/',views.userLogout,name="userLogout"),


    #student
    path('Add_Student/',views.Add_Student,name="Add_Student"),
    path('viewCourse/',views.viewCourse,name="viewCourse"),





    #serializers urls
    path('User_ViewPost/',User_ViewPost.as_view(), name="User_ViewPost"),
    path('Student_ViewPost/',Student_ViewPost.as_view(), name="Student_ViewPost"),

    


    #STUDENTS
    path('Student_StdGet/',Student_StdGet.as_view(), name="Student_StdGet"),


    #COURSE
    path('CouserViewPost/',CouserViewPost.as_view(), name="CouserViewPost"),
    path('CouserUpdate/',CouserUpdate.as_view(), name="CouserUpdate"),
    path('CourseSearch/',CourseSearch.as_view(), name="CourseSearch"),

    #SUBJECT
    path('SubjectUpdate/',SubjectUpdate.as_view(), name="SubjectUpdate"),




    # path('CourseViewUpdate',CourseViewUpdate.as_view(), name="CourseViewUpdate"),

   ]
