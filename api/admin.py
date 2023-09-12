from django.contrib import admin

from .models import Course, CourseEnrollment, CustomUser, Message, Section, TeacherProfile, Video

# Register your models here.


admin.site.register(CustomUser)
admin.site.register(TeacherProfile)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Video)
admin.site.register(CourseEnrollment)
admin.site.register(Message)


