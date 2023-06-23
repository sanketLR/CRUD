from rest_framework import serializers
from . models import *
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError, transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from django.contrib.auth.hashers import make_password
from . decoretor import *

#new line added

class SuperUserSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = CustomUser
        fields = ['id','username','email','phone','password','address','is_superuser','is_staff']

class UserSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = CustomUser
        fields = ['id','username','email','phone','password','address']
    
    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        
        if self.instance and self.instance.username != username and CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists")
        
        if self.instance and self.instance.email != email and CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        
        return attrs
    
class CouserBulkUpdateSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        print("INSTANCE DATA",instance) #data from data base queryset[]
        print("VALIDATED DATA",validated_data) #data from payload , list of dict
        instance_hash = {index: i for index, i in enumerate(instance)}
        print("instance_hash TYPE",type(instance_hash))
        print("instance_hash",instance_hash)
        result = [
            self.child.update(instance_hash[index], attrs) for index, attrs in enumerate(validated_data)
                
        ]
        print("self.child.Meta",self.child.Meta.fields)
        print("result",result)
        try:
            Course.objects.bulk_update(result, ['name'])
            print("HIT BULK UPDATE")
        except IntegrityError as e:  
              raise ValidationError(e)  
            # pass
        return result
    
class CourseUpdateSerializer(serializers.ModelSerializer):
    def validate(self,data):
        if len(data['name']) > 10:
            print(len(data['name']))
            raise serializers.ValidationError("Course Name is too lengthy")  
        return data
    class Meta:
        model = Course
        fields = '__all__'
        list_serializer_class = CouserBulkUpdateSerializer    
    
class CouserBulkCreateUpdateSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        print("validated_data",validated_data)

        course_data = [Course(**item) for item in validated_data]

        return Course.objects.bulk_create(course_data)
    
class CourseSerializer(serializers.ModelSerializer):

    def validate(self,data):
        if len(data['name']) > 10:
            print(len(data['name']))
            raise serializers.ValidationError("Course Name is too lengthy")  
        return data

    class Meta:
        model = Course
        fields = '__all__'
        list_serializer_class = CouserBulkCreateUpdateSerializer
        depth = 1
        validators = [
            UniqueTogetherValidator(queryset=Course.objects.all(), fields=['name'], message='Course with this name already exists.')
        ]    

class StudentViewSerializer(serializers.ModelSerializer):
    name = UserSerializer()
    related_course = CourseSerializer()
    class Meta:
        model = Student
        fields = ['id','roll_no','std','user_tag','related_course','name']

class SubjectBulkUpdateSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        print("INSTANCE DATA",instance) #data from data base queryset[]
        print("VALIDATED DATA",validated_data) #data from payload , list of dict
        for i in instance:
            print("I", i)
            instance_hash = {index: j for index, j in enumerate(i)}
            
        # instance_hash = {index: i for index, i in enumerate(instance)}
        print("instance_hash TYPE",type(instance_hash))
        print("instance_hash",instance_hash)
        result = [
            self.child.update(instance_hash[index], attrs) for index, attrs in enumerate(validated_data)
                
        ]
        print("self.child.Meta",self.child.Meta.fields)
        print("result",result)
        try:
            Subject.objects.bulk_update(result, ['name'])
            print("HIT BULK UPDATE")
        except IntegrityError as e:  
              raise ValidationError(e)  
            # pass
        return result
    
class SubjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        list_serializer_class = SubjectBulkUpdateSerializer
        
class SubjectBulkCreateSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        print("VALIDATED DATA", validated_data)
        subject_data= [Subject(**item) for item in validated_data]
        print("subject_data",subject_data)
        return Subject.objects.bulk_create(subject_data) 

class SubjectSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = Subject
        fields = ['id','name','course']
        depth = 1
        list_serializer_class = SubjectBulkCreateSerializer
        validators = [
            UniqueTogetherValidator(
                queryset=Subject.objects.all(),
                fields=['name'],
                message='Subject with this name already exists'
            )
        ]        

class StudentBulkUpdateSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        
        # print("INSTANCE DATA",instance) #data from data base queryset[]
        # print("validated_data",validated_data)
        for i in instance:
            # print("I", i)
            instance_hash = {index: j for index, j in enumerate(i)}
        # print("instance_hash",instance_hash)
        result = [
            self.child.update(instance_hash[index], attrs) for index, attrs in enumerate(validated_data)
                
        ]
        # print("result",result)
       
        try:
            Student.objects.bulk_update(result, ['roll_no','user_tag','std'])
            # print("HIT BULK UPDATE")
        except IntegrityError as e:  
              raise ValidationError(e)  
            # pass
        return result

#STUDENT UPDATE
# class StudentUpdateSerializer(serializers.ModelSerializer):
#     name = UserSerializer()
#     related_course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
#     class Meta:
#         model = Student
#         fields = ['related_course','name','roll_no','user_tag','std']
#         list_serializer_class = StudentBulkUpdateSerializer
        
#     def update(self, instance, validated_data):
#         # print("instance =====",instance)
#         name_data = validated_data.pop('name',None)
#         # print("name_data",name_data)
#         if name_data:
#             name_serializer = UserSerializer(instance.name, data=name_data)
#             print("name serializer",name_serializer )

#             if name_serializer.is_valid():
#                 name_serializer.save()
#             else:
#                 # 
#                 pass

#         return super().update(instance, validated_data)

class StudentUpdateSerializer(serializers.ModelSerializer):
    name = UserSerializer()
    related_course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Student
        fields = ['related_course', 'name', 'roll_no', 'user_tag', 'std']

    def update(self, instance, validated_data):
        name_data = validated_data.pop('name', None)

        if name_data:
            user_instance = instance.name
            user_serializer = UserSerializer(user_instance, data=name_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()

        return super().update(instance, validated_data)

    def bulk_update(self, queryset, validated_data_list):
        instance_dict = {instance.id: instance for instance in queryset}
        update_list = []
        for validated_data in validated_data_list:
            instance_id = validated_data['id']
            instance = instance_dict.get(instance_id)
            if instance:
                serializer = self.__class__(instance, data=validated_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    update_list.append(serializer.instance)
        return update_list
    
class StudentBulkCreateSerializer(serializers.ListSerializer):
    
    def create(self, validated_data):
                
        cust_user_valid_lst = []
        course_valid_lst = []
        student_valid_lst = []
        for sub_validated_data in validated_data:
            cust_user_valid_lst.append(sub_validated_data.pop('name'))
            course_valid_lst.append(sub_validated_data.pop('related_course'))
            student_valid_lst.append(sub_validated_data)
        
        unique_combination = {}
        index_lst = []
        '''fetching index of duplicate std & roll_no from list'''
        for index, stud_data in enumerate(student_valid_lst):
            roll_no = stud_data['roll_no']
            std = stud_data['std']
            combination = (roll_no, std)
            if combination in unique_combination:
                # raise ValidationError("THE COMBINATION IS ALREADY EXISTS")
                index_lst.append(index)
                continue
            unique_combination[combination] = index

        print("index_lst ===>",index_lst)
        new_cust_user_valid_lst = []
        new_course_valid_lst = []
        new_student_valid_lst = []
        
        '''removing duplicate std & roll_no data frol list'''
        for user_index,new_CustUserData in enumerate(cust_user_valid_lst):
            if user_index in index_lst:
                del new_CustUserData
            else:
                new_cust_user_valid_lst.append(new_CustUserData)

        for course_index,new_CourseData in enumerate(course_valid_lst):
            if course_index in index_lst:
                del new_CourseData
            else:
                new_course_valid_lst.append(new_CourseData)

        for student_index,new_StudentData in enumerate(student_valid_lst):
            if student_index in index_lst:
                del new_StudentData
            else:
                new_student_valid_lst.append(new_StudentData)

        cust_user_lst = [CustomUser(**userData) for userData in new_cust_user_valid_lst ]
        for cust_password in cust_user_lst:
            cust_password.password = make_password(cust_password.password, hasher='argon2')
            # cust_password.make(cust_password.password)    
        all_Custom_Users = CustomUser.objects.bulk_create(cust_user_lst)
        student_lst = [Student(**studData , name = all_Custom_Users[INDEX],related_course = new_course_valid_lst[INDEX] ) for INDEX,studData in enumerate(new_student_valid_lst) ]

        return Student.objects.bulk_create(student_lst)


#STUDENT CREATE
class StudentSerializer(serializers.ModelSerializer):
    print("19 ======== 19")
    name = UserSerializer()
    related_course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    print("22")

    class Meta:
        model = Student
        # fields = '__all__'
        fields = ['id','roll_no','std','user_tag','related_course','name']
        depth = 2
        list_serializer_class = StudentBulkCreateSerializer
        validators = [
            UniqueTogetherValidator(
                queryset=Student.objects.all(),
                fields=['roll_no','std'],
                message='The combination of standerd and roll number is already exists'
            )
        ]









##########################################################
#PREVIOUS CODE [MULTIPLE HIT]


    # @transaction.atomic
    # def create(self, validated_data):
    #     name_data = validated_data.pop('name')
    #     print(name_data)
    #     course_data = validated_data.pop('related_course')
    #     course_id = course_data.id
    #     print("course_data",course_data.id)
    #     # print('course_data',course_data['id'])
    #     with transaction.atomic():
    #         user = CustomUser.objects.create(**name_data)
    #         user.set_password(user.password)

    #     sid = transaction.savepoint()
    #     try:
    #         course = Course.objects.get(id = course_id)
    #     except Course.DoesNotExist as e:
    #         return Response({'status':status.HTTP_400_BAD_REQUEST, 'msg':'This Course does not exists', 'payload':e})
    #     student = Student.objects.create(name=user,related_course =course, **validated_data)
    #     if student:
    #         transaction.savepoint_commit(sid)
    #     else:
    #         transaction.savepoint_rollback(sid)
    #     return student





# class CouserBulkCreateUpdateSerializer(serializers.ListSerializer):

#     def create(self, validated_data):
#         print("validated_data",validated_data)
#         # course_data = []
#         course_data = [Course(**item) for item in validated_data]
#         print("course_data",course_data)
#         return Course.objects.bulk_create(course_data)

    
#     def update(self, instance, validated_data):
#         instance_hash = {index: i for index, i in enumerate(instance)}
#         result = [
#             self.child.update(instance_hash[index], attrs)
#             for index, attrs in enumerate(validated_data)
#         ]
#         writable_fields = [
#             x
#             for x in self.child.Meta.fields
#             if x not in self.child.Meta.read_only_fields
#         ]

#         try:
#             self.child.Meta.model.objects.bulk_update(result, writable_fields)
#         except:
#             pass

#         return result
    
