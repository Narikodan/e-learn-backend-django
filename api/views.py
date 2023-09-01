from rest_framework import generics
from rest_framework.response import Response
from .models import Course, CustomUser
from .serializers import CustomTokenObtainPairSerializer, UserRegistrationSerializer, UserDataSerializer, CourseSerializer
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
