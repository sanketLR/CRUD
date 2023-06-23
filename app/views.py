from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login,logout
from .decoretor import unauthenticated_user,superuser_validate
from . models import *
# Create your views here.

@unauthenticated_user
def home(request):
    return render(request,'app/home.html')

@superuser_validate
def RegisterUser(request):
    try: 
        data = CustomUser.objects.all()
    except CustomUser.DoesNotExist:
        pass
    if request.method == "POST":
        form = UserForm(data = request.POST)
        if form.is_valid():
            messages.success(request,'Register successfully')
            form.save()
            return redirect('RegisterUser')
        else:
            print(form.errors)
            return redirect('RegisterUser')
    else:
        form = UserForm()
    context = {
        'form':form,
        'data':data
    }
    return render(request,'register_users.html',context)



def UserLogin(request):
    if request.user.is_authenticated == False:
        form = LoginForm()
        if request.method == "POST":
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user= authenticate(request, username = username, password = password)
                if user:
                    login(request,user)
                    messages.success(request,'You are logged in successfully')
                    return redirect('home')
                else:
                    messages.error(request,'Can not login, Try again')
                   
                    return redirect('UserLogin')
            
        context = {
            'form':form
        }
        return render(request,'UserLogin.html',context)
    else:
        return redirect('home')
    


@unauthenticated_user
def userLogout(request):
    logout(request)
    return redirect('UserLogin')
    # return render(request,'registration/logged_out.html')
    
@unauthenticated_user
def Add_Student(request):
    data = Student.objects.all()
    course = Course.objects.all()
    if request.method == "POST":
        username = request.POST.get('username')
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        roll_no = request.POST.get('roll_no')
        std = request.POST.get('std')
        address = request.POST.get('address')
        course = request.POST.get('course')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        try:
            cur_course = Course.objects.get(name = course)
        except Course.DoesNotExist:
            messages.error(request,'Course does not exists')
            return redirect('Add_Student')
        if password1  == password2:
            pass
        else:
            messages.warning(request,'Password does not match')
            return redirect('Add_Student')
        user = CustomUser(
            username = username,
            # first_name = first_name,
            # last_name =last_name,
            email = email,
            phone = phone,
            address = address,
            password = password2
        )
        if CustomUser.objects.filter(username = username).exists():
            messages.warning(request,'Username already exits')
            return redirect('Add_Student')
        if CustomUser.objects.filter(email = email).exists():
            messages.warning(request,'email already exits')
            return redirect('Add_Student')
        user.set_password(password2)
        user.save()
        print("➡ user data addedd successfully :")
        student = Student(
            name = user,
            roll_no = roll_no,
            std = std,
            related_course = cur_course
        )
        if Student.objects.filter(roll_no = roll_no, std = std).exists():
            messages.warning(request,f'studet with {roll_no} alread exits')
            return redirect('Add_Student')
        student.save()
        print("➡ student data addedd successfully :")
        messages.success(request,'Student addedd successfully')
        return redirect('Add_Student')
    
    context = {
        'data':data,
        'course':course
    }
    return render(request,'app/student/add_student.html',context)

@unauthenticated_user
def viewCourse(request):
    if request.user.is_authenticated == True:
        data = Course.objects.all()
        form = CourseForm()
        if request.method == "POST":
            form = CourseForm(data=request.POST)
            if form.is_valid():
                messages.success(request,'Course Create successfully')
                form.save()
                return redirect('viewCourse')
            else:
                messages.warning(request,'ERROR')
                
        context = {
            "data":data,
            'form':form
        }
        return render(request,'app/courses/add_course.html',context)
    else:
        return redirect('UserLogin')