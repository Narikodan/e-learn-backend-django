from django.contrib import admin

<<<<<<< HEAD
from .models import ChatRoom, Course, CourseEnrollment, CustomUser, Message, Section, TeacherProfile, Video
=======
from .models import Course, CourseEnrollment, CustomUser, Message, Section, TeacherProfile, Video
>>>>>>> 78728080fa113e75908e867dbecb0b029f6c622d

# Register your models here.


admin.site.register(CustomUser)
admin.site.register(TeacherProfile)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Video)
admin.site.register(CourseEnrollment)
<<<<<<< HEAD
admin.site.register(ChatRoom)
=======
>>>>>>> 78728080fa113e75908e867dbecb0b029f6c622d
admin.site.register(Message)


