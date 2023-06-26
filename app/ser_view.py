from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from . serializers import *
from rest_framework import status
from django.db import IntegrityError, transaction
from rest_framework import generics
from django.db import connection
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter

#ADMIN
class User_ViewPost(APIView):
    def get(self, request):
        obj = CustomUser.objects.filter(is_superuser = True)
        serializer = SuperUserSerializer(obj, many=True)
        return Response({'msg':'data ', 'payload':serializer.data, 'status':status.HTTP_200_OK})
        # return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = SuperUserSerializer(data = request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.set_password(instance.password)
            instance.save()
            return Response({'msg':'New User Add', 'payload':serializer.data, 'status':status.HTTP_200_OK})
        else:
            return Response({'msg':'Data not added', 'payload':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
        












#COURSE GET & POST (bulk_create)
class CouserViewPost(APIView):
    def get(self, request):
        obj = Course.objects.all()
        serializer = CourseSerializer(obj, many=True)
        return Response(serializer.data)


    def post(self, request):
        data = request.data
        print('request.data',request.data)
        course_lst = []
        
        print("POST METHOD CALLED IN COURSEVIEWPOST")
        serializer = CourseSerializer(data= request.data, many=True)
        print("serializer",serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'data added successfully','payload':serializer.data, 'status':status.HTTP_200_OK})
        else:
            return Response({'msg':'ERROR','payload':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})


class CourseSearch(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

#COURSE PUT & PATCH FOR (bulk_update)
class CouserUpdate(APIView):
    
    filter_backends = [SearchFilter]
    search_fields = ['name']
    def get(self, request):
        obj = Course.objects.all()
        serializer = CourseUpdateSerializer(obj, many=True)
        return Response(serializer.data)

    def put(self, request):
        # print("Reqeust.data", request.data)
        course_name =[]
        for i in request.data:
            # print(i['name'])
            # course_name.append(i['name'])
            course_name.append(
                {"name":i['name']}
            )
        # print('course_name',course_name)
        course_id_lst = []

        for data_id in request.data:
            course_id_lst.append(data_id['id'])
        # print("course_id_lst",course_id_lst)

        courses = Course.objects.filter(pk__in=course_id_lst)
        # print("courses",courses)

        serializer = CourseUpdateSerializer(courses,   data = course_name, many=True,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'update','payload': serializer.data, 'status': status.HTTP_200_OK})
        else:
            print(serializer.errors)
            return Response({'msg': 'Error', 'payload': serializer.errors,'status': status.HTTP_200_OK})
        
    def patch(self, request):
        data = request.data
        print("pathc data", data)
        course_name = []
        for i in request.data:
            course_name.append(
                {'name':i['name']}
            )
        
        course_id_lst = []
        for data_id in request.data:
            course_id_lst.append(data_id['id'])

        courses = Course.objects.filter(id__in = course_id_lst)
        serializer = CourseUpdateSerializer(courses, data=course_name, many=True, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial Update','payload':serializer.data, 'status':status.HTTP_200_OK})
        else:
            return Response({'msg':'ERROR', 'payload':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

class Student_ViewPost(APIView):
    filter_backends = [SearchFilter]
    search_fields = ['name']
    def get(self, request):
        obj = Student.objects.all()
        serializer = StudentViewSerializer(obj, many = True)
        print(serializer)
        if serializer.data:
            return Response(serializer.data )
        else:
            return Response({'msg':'no data avaliable'} )
        
    def post(serlf, request):
        student_data = request.data
        serializer = StudentSerializer(data=student_data, many= True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Added Successfully', 'payload':serializer.data, 'status':status.HTTP_200_OK})
        else:
            return Response({'msg':'ERROR','payload':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

    # def put(self, request):
    #     data = request.data

    #     customUser_id = []
    #     studUser_id = []

    #     for stud_id in data:
    #         studUser_id.append(stud_id['id'])


    #     studentobj = [Student.objects.filter(id__in = studUser_id)]
    #     # print(studentobj)
    #     # print(data)
    #     serializer = StudentUpdateSerializer(studentobj, data = data, many=True)
        
    #     if serializer.is_valid():
    #         # print("➡ serializer :", serializer)
    #         serializer.save()
    #         return Response({'msg':'Student data updated', 'payload':serializer.data, 'status':status.HTTP_200_OK})
    #     else:
    #         return Response({'msg':'ERROR', 'payload':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
    
    def put(self, request):
        data = request.data
        for i in data:
            print(i['id'])
        student_ids = [item['id'] for item in data]
        queryset = Student.objects.filter(id__in=student_ids)
        print("queryset",queryset)
        serializer = StudentUpdateSerializer()
        updated_instances = serializer.studupdate(queryset, data)

        if updated_instances:
            updated_serializer = StudentViewSerializer(updated_instances, many=True)
            return Response({'msg': 'Student data updated', 'payload': updated_serializer.data, 'status': status.HTTP_200_OK})
        else:
            return Response({'msg': 'No students updated', 'status': status.HTTP_400_BAD_REQUEST})
            
#PERTICULAR UPDATE
class Student_StdGet(APIView):
    def get(self, request):
        try:
            obj = Student.objects.filter(std = '12')
        except Student.DoesNotExist:
            return Response({'msg':'Data does not exists','status':status.HTTP_400_BAD_REQUEST})
        serializer = StudentSerializer(obj, many = True)
        return Response({'msg':'data found', 'payload':serializer.data, 'status':status.HTTP_200_OK})
    
    def put(self, request,*args, **kwargs):
        try:
            obj = Student.objects.filter(std = '12')
        except Student.DoesNotExist:
            return Response({'msg':'Data does not exists','status':status.HTTP_400_BAD_REQUEST})
        for studData in request.data:
            # print(studData)
            # print("➡ studData :", studData)
            student_data = studData['CustomUserStud']
            for data in student_data:
                print(data)
            # for data in studData['CustomUserStud']:
            #     print(data)
            #     # print("➡ data :", data)
        for stud_obj in obj:
            for stud_data in request.data:
                stud_data['std'] = '11'
                serializer = StudentSerializer(stud_obj, stud_data['CustomUserStud'])
                # print('stud_obj',stud_obj)
                # print(serializer)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors)
        

class SubjectUpdate(APIView):
    def get(self, request):
        obj = Subject.objects.all()
        serializer = SubjectSerializer(obj, many=True)
        return Response({'msg':'Data found','paylaod':serializer.data,'status':status.HTTP_200_OK})
        
    def post(self, request):
        data = request.data
        serializer = SubjectSerializer(data = data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Subject add', 'payload':serializer.data,'status':status.HTTP_200_OK})
        else:
            return Response({'msg':'ERROR', 'payload':serializer.errors,'status':status.HTTP_400_BAD_REQUEST})

    def put(self, request):
        subject_id_lst = []
        data = request.data
        for subjectData in data:
            subject_id_lst.append(subjectData['id'])

        subject_obj_lst = [Subject.objects.filter(id__in= subject_id_lst)]
        serializer = SubjectUpdateSerializer(subject_obj_lst, data = data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Updated', 'payload':serializer.data, 'status':status.HTTP_200_OK})
        else:
            return Response({'msg':'ERROR', 'payload':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

# class Student_ViewPost(APIView):
#     def get(self, request):
#         try:
#             obj = Student.objects.all()
#             # obj1 = Student.objects.all()
#         except:
#             return Response({'msg':'data not found', 'payload': serializer.errors})
#         serializer = StudentSerializer(obj, many = True)
#         # serializer1 = StudentSerializer(obj, many = True)
#         return Response({'msg':'data found','payload':serializer.data , 'status':status.HTTP_200_OK})
        
#     def post(self, request):
#         user_data = request.data['user']
#         stud_data = request.data['CustomUserStud']
#         serializer1 = UserSerializer(data = user_data)
#         serializer2 =StudentSerializer(data = stud_data)
#         print(serializer2)

#         if serializer1.is_valid():
           
           
#             instance = serializer1.save()
#             instance.set_password(instance.password)
#             print(instance)
#             get_id = instance.id
#             print(get_id)
            
#         stud_data['user'] = get_id
#         if serializer2.is_valid():
#             serializer2.save()
#             print("serializer2.data",serializer2.data)
#             return Response({'msg':'New User Add', 'payload1':serializer1.data, 'payload2':serializer2.data, 'status':status.HTTP_200_OK})
        
#         else:
#             return Response({'msg':'Data not added', 'payload1':serializer1.errors,'payload2':serializer2.errors, 'status':status.HTTP_400_BAD_REQUEST})
        



# class Student_ViewPost(APIView):
#     def get(self, request):
#         try:
#             obj = Student.objects.all()
#             # obj1 = Student.objects.all()
#         except:
#             return Response({'msg':'data not found', 'payload': serializer.errors})
#         serializer = StudentSerializer(obj, many = True)
#         # serializer1 = StudentSerializer(obj, many = True)
#         return Response({'msg':'data found','payload':serializer.data , 'status':status.HTTP_200_OK})
        
#     def post(self, request):
#         # user_data = request.data['user']
#         # stud_data = request.data['CustomUserStud']
#         # print(request.data)
#         id_lst = []
#         for i in request.data:

#             # for ser1 in i['user']:
#             # print(ser1)
#             u_ser = UserSerializer(data = i['user'])
#             user_lst = []
#             if u_ser.is_valid():
#                 user_lst.append(u_ser)
#                 instance = u_ser.save()
#                 instance.set_password(instance.password)
#                 get_id = instance.id

#             s_id = i['CustomUserStud']
#             s_ser = StudentSerializer(data = i['CustomUserStud'])
#             s_id['user'] = get_id
#             if s_ser.is_valid():
#                 s_ser.save()
#                 print(s_ser['roll_no'])
#                 print(s_ser['user_tag'])
#             # id_lst.append(get_id)
#                     # Response({'payload':u_ser.data})
           
                    
#         return Response({'msg':'New User Add', 'payload1':u_ser.data, 'payload1':s_ser.data,'status':status.HTTP_200_OK})