from rest_framework import generics
from rest_framework.response import Response
from .models import Course, CustomUser, Section, TeacherProfile
from .serializers import CourseCreationSerializer, CustomTokenObtainPairSerializer, SectionAddSerializer, SectionSerializer, UserRegistrationSerializer, UserDataSerializer, CourseSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import api_view



class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'success'})
        return Response({'message': 'failed'})
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer 

class UserDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserDataSerializer(user)  # Serialize the user data
        return Response(serializer.data) 
    
class CourseCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

from django.http import JsonResponse

def courses_by_category(request):
    category = request.GET.get('category')
    if category:
        courses = Course.objects.filter(category=category)
        serialized_courses = CourseSerializer(courses, many=True)
        return JsonResponse(serialized_courses.data, safe=False)
    else:
        return JsonResponse({'error': 'Category parameter is missing'}, status=400)
    
from rest_framework import generics
from rest_framework import permissions
from .models import Course
from .serializers import CourseSerializer

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Course
from .serializers import CourseCreationSerializer

class CreateCourseView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Check if the user is a teacher
        user = self.request.user
        if not hasattr(user, 'teacherprofile'):
            # User is not a teacher, create a TeacherProfile for them
            teacher_profile = TeacherProfile.objects.create(user=user, qualifications='')
        else:
            # User is already a teacher
            teacher_profile = user.teacherprofile

        # Associate the teacher profile with the course
        serializer.save(teacher=teacher_profile)


class SectionCreateView(generics.CreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionAddSerializer

    def get_queryset(self):
        # Filter courses by the user creating the section.
        user = self.request.user
        return Course.objects.filter(teacher__user=user)

    def perform_create(self, serializer):
        # Automatically set the course to the selected course.
        user = self.request.user
        selected_course_id = self.request.data.get('course')
        course = Course.objects.get(id=selected_course_id, teacher__user=user)
        serializer.save(course=course)

class UserCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(teacher__user=user)