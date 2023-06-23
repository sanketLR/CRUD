from typing import Any, Optional
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.admin import UserAdmin
from django.db.models import Avg
from django.utils.http import urlencode
from django.utils.html import format_html
# Register your models here.
from . models import *

# admin.site.register(Stud)
# admin.site.register(Book)
# admin.site.register(Stationery)

class CustUsersAdmin(UserAdmin):
    list_display = ['username', 'email']
    
admin.site.register(CustomUser,CustUsersAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ['name','related_course', 'standard', 'student_roll_no']
    ordering = ['-std', 'roll_no']
    list_filter = ['related_course', 'std', ]
    search_fields = ['name__username__istartswith', 'related_course__name', 'std']
    fields = ('name','related_course','roll_no','std','user_tag')

    def get_form(self, request, obj, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].label = "Select your name"
        return form

    def standard(self, obj):
        return obj.std
    
    def student_roll_no(self, obj):
        print(obj.name.phone)
        print(obj.name.address)
        print(obj.related_course)
        return format_html('<h3 align="center"><b>{}</b></h3>', obj.roll_no)

admin.site.register(Student,StudentAdmin)

class CourseAdmin(admin.ModelAdmin):
    list_display = ['name','link_to_student','link_to_course']
    list_filter = ['name']
    def link_to_student(self, obj):
        # print(obj.id)
        count = obj.student_set.count()
        url = (
            reverse("admin:app_student_changelist")
            + "?"
            + urlencode({"course__id" : f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Student</a>', url, count)
    
    link_to_student.short_description = "Student"

    def link_to_course(self, obj):
        # print(obj.id)
        count = obj.subject_set.count()
        url = (
            reverse("admin:app_subject_changelist")
            + "?"
            + urlencode({"course__id" : f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Subject</a>', url, count)
    
    link_to_course.short_description = "Subject"

    # ordering = ['id']

admin.site.register(Course,CourseAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    
   
admin.site.register(Subject,SubjectAdmin)

admin.site.register(Staff)