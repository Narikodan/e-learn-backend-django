from . import views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CreateCourseView, SectionCreateView, UserCoursesViewSet, UserDataView, UserRegistrationView, CustomTokenObtainPairView, CourseCategoryViewSet
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

    
]
