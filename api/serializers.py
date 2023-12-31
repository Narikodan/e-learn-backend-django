from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

<<<<<<< HEAD
from .models import ChatRoom, Course, CustomUser, Message, Section, TeacherProfile, Video
=======
from .models import Course, CustomUser, Message, Section, TeacherProfile, Video
>>>>>>> 78728080fa113e75908e867dbecb0b029f6c622d

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password')
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        failed = {"message":"failed"}

        user = authenticate(email=email, password=password)
        if user:
            data = super().validate(attrs)
            data['message'] = 'success'
            return data
        else:
            return failed
        

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name')  # Include other user data fields as needed


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id','title', 'video_url')  # Include other video-related fields as needed

class SectionSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True)  # Include videos within the section serializer

    class Meta:
        model = Section
        fields = ('id', 'title', 'videos')  # Include other section-related fields as needed



class TeacherProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = TeacherProfile
        fields = ('id', 'qualifications', 'full_name')

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherProfileSerializer()
    sections = SectionSerializer(many=True) 
    class Meta:
        model = Course
        fields = ('id', 'category', 'title', 'description', 'teacher', 'sections')

class CourseCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['category', 'title', 'description', 'teacher']
        read_only_fields = ['teacher']

    def create(self, validated_data):
        # You can add custom logic here if needed before creating the course.
        return Course.objects.create(**validated_data)
    
class SectionAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = ('title', 'course')  # Include other section-related fields as needed

class VideoAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'section', 'video_url']



class UserCoursesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'category', 'title', 'description')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('title', 'video_url')

class SectionSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True)

    class Meta:
        model = Section
        fields = ('id', 'title', 'videos')

class CourseDetailSerializer(serializers.Serializer):
    sections = SectionSerializer(many=True)


class CourseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['category', 'title', 'description']

class SectionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['title']

class VideoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'video_url']


class SearchResultsSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True)  # Include sections within the search results
    teacher = TeacherProfileSerializer()
    class Meta:
        model = Course
        fields = ('id', 'category', 'title', 'description', 'teacher', 'sections')



class CourseEnrollmentSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()

class EnrolledCourseSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True)  # Include sections within the search results
    teacher = TeacherProfileSerializer()
    class Meta:
        model = Course
        fields = ('id', 'category', 'title', 'description', 'teacher', 'sections')

# serializers.py

from rest_framework import serializers
from .models import PasswordResetRequest

class PasswordResetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetRequest
        fields = ['user', 'token']
        read_only_fields = ['token']

    def create(self, validated_data):
        user = validated_data['user']
        # Generate a unique token (you can use Django's built-in token generator)
        token = ...  # Generate a token here
        reset_request = PasswordResetRequest.objects.create(user=user, token=token)
        return reset_request
    
class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=100)
    new_password = serializers.CharField(write_only=True)

    def validate_token(self, value):
        # Check if the token is valid (e.g., not expired and exists in the database)
        # You can add your validation logic here
        return value
    

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['subject', 'content']





class ChatRoomSerializer(serializers.ModelSerializer):
    users = UserDataSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ('id', 'users')

class MessageSerializer(serializers.ModelSerializer):
    sender = UserDataSerializer()

    class Meta:
        model = Message
        fields = ('id', 'sender', 'chat_room', 'content', 'timestamp')

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'content', 'timestamp')

