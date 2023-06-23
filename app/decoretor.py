from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages 
from rest_framework.response import Response

def Duplicate_rno_std(view_func):
    def wrapper_func( request, *args, **kwargs):
        if request.validated_data:
            print("YES DECORATER")
        else:
            print("NO DECORATER")
            return view_func(request, *args, **kwargs)
    return wrapper_func


def unauthenticated_user(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated == False:
            messages.error(request,'Login Required')
            return redirect('UserLogin')
        else: 
            return view_func(request, *args, **kwargs)
    return wrapper_func

def superuser_validate(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser == False:
            messages.error(request,'Please login as superuser')
            return redirect('UserLogin')
        else: 
            return view_func(request, *args, **kwargs)
    return wrapper_func
            




def superUser_access(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser == False:
            messages.error(request,'Only Admin can access')
            return redirect('UserLogin')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func