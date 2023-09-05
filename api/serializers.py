from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

from .models import Course, CustomUser, Section, TeacherProfile, Video

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
        fields = ('title', 'video_url')  # Include other video-related fields as needed

class SectionSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True)  # Include videos within the section serializer

    class Meta:
        model = Section
        fields = ('title', 'videos')  # Include other section-related fields as needed



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