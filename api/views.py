from rest_framework import generics
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from .models import Course, CustomUser, Section, TeacherProfile, Video
from .serializers import CourseCreationSerializer, CourseDetailSerializer, CourseUpdateSerializer, CustomTokenObtainPairSerializer, SearchResultsSerializer, SectionAddSerializer, SectionSerializer, SectionUpdateSerializer, UserCoursesListSerializer, UserRegistrationSerializer, UserDataSerializer, CourseSerializer, VideoAddSerializer, VideoUpdateSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from .models import Course, Section, Video
from rest_framework import generics, permissions
from rest_framework import status
from django.shortcuts import get_object_or_404





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
    

class VideoCreateView(generics.CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoAddSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter sections by the user creating the video.
        user = self.request.user
        return Section.objects.filter(course__teacher__user=user)

    def perform_create(self, serializer):
        # Automatically set the section to the selected section.
        user = self.request.user
        selected_section_id = self.request.data.get('section')
        section = Section.objects.get(id=selected_section_id, course__teacher__user=user)
        serializer.save(section=section)

class UserSectionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Section.objects.filter(course__teacher__user=user)
    
class UserCoursesListView(generics.ListAPIView):
    serializer_class = UserCoursesListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user  # Get the current user
        return Course.objects.filter(teacher__user=user)
    
class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'  # Use 'id' as the lookup field for the course ID

class CourseUpdateView(RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CourseUpdateSerializer

class SectionUpdateView(RetrieveUpdateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionUpdateSerializer

class VideoUpdateView(RetrieveUpdateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoUpdateSerializer




class CourseDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)

        if request.user == course.teacher.user:
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

class SectionDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, section_id):
        section = get_object_or_404(Section, pk=section_id)

        # Add any additional permission checks here if needed
        section.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VideoDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, video_id):
        video = get_object_or_404(Video, pk=video_id)

        # Add any additional permission checks here if needed
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework import generics, filters
from django.db.models import Q

class CourseSearchAPIView(generics.ListAPIView):
    serializer_class = SearchResultsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'sections__title', 'sections__videos__title']

    def get_queryset(self):
        query = self.request.GET.get('q', '')  # Get the search keyword from the query parameter
        return Course.objects.filter(
            Q(title__icontains=query) |  # Search in the course title
            Q(description__icontains=query) |  # Search in the course description
            Q(sections__title__icontains=query) |  # Search in section titles
            Q(sections__videos__title__icontains=query)  # Search in video titles within sections
        ).distinct()
