from . import views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CourseDetailView, CreateCourseView, PasswordResetRequestView, PasswordResetView, SectionCreateView, UserCoursesListView, UserCoursesViewSet, UserDataView, UserRegistrationView, CustomTokenObtainPairView, CourseCategoryViewSet, UserSectionsViewSet, VideoCreateView
from rest_framework.routers import DefaultRouter

app_name = 'api'

# Create a router for the CourseCategoryViewSet
router = DefaultRouter()
router.register(r'course-categories', CourseCategoryViewSet)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('user-data/', UserDataView.as_view(), name='user-data'),
    path('', include(router.urls)),
    path('courses-by-category/', views.courses_by_category, name='courses_by_category'),
    path('create-course/', CreateCourseView.as_view(), name='create-course'),
    path('create-section/', SectionCreateView.as_view(), name='create-section'),
    path('user-courses/', UserCoursesViewSet.as_view({'get': 'list'}), name='user-courses'),
    path('create-video/', VideoCreateView.as_view(), name='create-video'),
    path('user-sections/', UserSectionsViewSet.as_view({'get': 'list'}), name='user-sections'),
    path('user-courses/', UserCoursesListView.as_view(), name='user-courses-list'),
    path('course-detail/<int:id>/', CourseDetailView.as_view(), name='course-detail'),
    path('update-course/<int:pk>/', views.CourseUpdateView.as_view(), name='update-course'),
    path('update-section/<int:pk>/', views.SectionUpdateView.as_view(), name='update-section'),
    path('update-video/<int:pk>/', views.VideoUpdateView.as_view(), name='update-video'),
    path('courses/<int:course_id>/delete/', views.CourseDeleteView.as_view(), name='delete_course'),
    path('sections/<int:section_id>/delete/', views.SectionDeleteView.as_view(), name='delete_section'),
    path('videos/<int:video_id>/delete/', views.VideoDeleteView.as_view(), name='delete_video'),
    path('search/', views.CourseSearchAPIView.as_view(), name='course-search'),
    path('enroll-course/', views.CourseEnrollmentView.as_view(), name='enroll-course'),
    path('enrolled-courses/', views.EnrolledCoursesView.as_view(), name='enrolled-courses'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('create-chat-room/', views.ChatRoomCreateView.as_view(), name='create-chat-room'),
    path('chat-rooms/<int:chat_room_id>/messages/', views.MessageListView.as_view(), name='chat-room-messages'),
    path('chat-rooms/<int:chat_room_id>/send-message/', views.MessageCreateView.as_view(), name='send-chat-message'),
    path('chat-rooms/', views.ChatRoomListView.as_view(), name='chat-room-list'),


    
]
