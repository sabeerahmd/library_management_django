from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf.urls.static import static
from library_management import settings

urlpatterns = [
    path('admin_signup',adminsignup,name = "adminsignup"),
    path('admin_login',adminlogin,name = "adminlogin"),
    path('',welcome,name = "welcome"),
    path('book_details',bookdetails,name = "bookdetails"),
    path('add_book',book_page,name = 'addbook'),
    path('updatebook/<pk>',updatebook,name='updatebook'),
    path('deletebook/<pk>',deletebook,name='deletebook'),
    path('student_signup',student_signup,name='studentsignup'),
    path('student_login',student_login,name = 'studentlogin'),
    path('take_book',take_book,name = 'takebook'),
    path('takebook/<pk>',takebook,name='takebook'),
    path('retainbook/<pk>',retainbook,name = 'retainbook' )

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)