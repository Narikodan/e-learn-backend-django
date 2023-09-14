from base64 import urlsafe_b64decode
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from .models import ChatRoom, Course, CourseEnrollment, CustomUser, Message, Section, TeacherProfile, Video
from .serializers import ChatRoomSerializer, CourseCreationSerializer, MessageCreateSerializer, MessageSerializer, PasswordResetRequest, CourseEnrollmentSerializer, CourseUpdateSerializer, CustomTokenObtainPairSerializer, EnrolledCourseSerializer, PasswordResetRequestSerializer, PasswordResetSerializer, SearchResultsSerializer, SectionAddSerializer, SectionSerializer, SectionUpdateSerializer, UserCoursesListSerializer, UserRegistrationSerializer, UserDataSerializer, CourseSerializer, VideoAddSerializer, VideoUpdateSerializer
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
from rest_framework import generics, filters
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import UpdateAPIView
from rest_framework import status
from rest_framework.response import Response





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
    


class CourseEnrollmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CourseEnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            course_id = serializer.validated_data['course_id']
            try:
                course = Course.objects.get(pk=course_id)
            except Course.DoesNotExist:
                return Response({'message': 'Course not found'})

            # Check if the user is already enrolled in the course
            if CourseEnrollment.objects.filter(student=request.user, course=course).exists():
                return Response({'message': 'already enrolled'})
            else:

                # Enroll the user in the course
                enrollment = CourseEnrollment(student=request.user, course=course)
                enrollment.save()

                return Response({'message': 'Enrollment successful'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EnrolledCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrolled_courses = CourseEnrollment.objects.filter(student=request.user).values_list('course', flat=True)
        courses = Course.objects.filter(pk__in=enrolled_courses)
        serializer = EnrolledCourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
import secrets
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, PasswordResetRequest
from .serializers import PasswordResetRequestSerializer, PasswordResetSerializer

class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Generate a secure token for the password reset
        token = secrets.token_urlsafe(32)  # Generate a 64-character random URL-safe token

        # Send a password reset email to the user with the token
        token_url = f'/password-reset?token={token}'  # Adjust the URL as needed
        mail_subject = 'Password Reset for Your Account'
        message = f'Use the following link to reset your password: {token_url}'
        send_mail(mail_subject, message, 'elearningknoweldgehub@gmail.com', [user.email])

        # Create a PasswordResetRequest entry in the database
        PasswordResetRequest.objects.create(user=user, token=token)

        return Response({'message': 'Password reset email sent successfully'})

class PasswordResetView(APIView):
    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        # Find the PasswordResetRequest entry by token
        try:
            reset_request = PasswordResetRequest.objects.get(token=token)
            user = reset_request.user
        except PasswordResetRequest.DoesNotExist:
            return Response({'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the user's password
        user.set_password(new_password)
        user.save()

        # Delete the used reset request
        reset_request.delete()

        return Response({'message': 'Password reset successfully'})


class ChatRoomCreateView(generics.CreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Get the teacher_id from the request data
        teacher_id = self.request.data.get('teacher_id')

        try:
            # Find the TeacherProfile with the specified teacher_id
            teacher_profile = TeacherProfile.objects.get(id=teacher_id)

            # Retrieve the associated CustomUser
            target_user = teacher_profile.user

            # Check if a chat room with the same users already exists
            existing_chat_room = ChatRoom.objects.filter(users=self.request.user).filter(users=target_user).first()

            if existing_chat_room:
                # Return the existing chat room's data
                serializer = ChatRoomSerializer(existing_chat_room)
                return Response({'chat_room': serializer.data, 'message': 'Chat room already exists'},
                                status=status.HTTP_200_OK)

            # Create the chat room with the current user and target user
            chat_room = serializer.save()
            chat_room.users.add(self.request.user, target_user)
            chat_room.save()
        
        except TeacherProfile.DoesNotExist:
            return Response({'error': 'Teacher profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({'error': 'CustomUser not found for the teacher'}, status=status.HTTP_404_NOT_FOUND)
            
        
            


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_room_id = self.kwargs['chat_room_id']
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        # Check if the current user is a member of the chat room
        if self.request.user in chat_room.users.all():
            return Message.objects.filter(chat_room=chat_room).order_by('timestamp')
        else:
            return Message.objects.none()

class MessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        chat_room_id = self.request.data.get('chat_room_id')
        chat_room = ChatRoom.objects.get(id=chat_room_id)

        # Set the sender to the authenticated user
        serializer.save(sender=self.request.user, chat_room=chat_room)
        
class ChatRoomListView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retrieve chat rooms for the current user
        return ChatRoom.objects.filter(users=self.request.user)

