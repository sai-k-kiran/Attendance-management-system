from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required



urlpatterns = [
	path('', views.home, name='home'),
	path(r'signin', auth_views.LoginView.as_view(template_name='login.html'), name='signin'),
    path('logout', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
	path(r'dashboard', views.dashboard, name='dashboard'),
	path(r'lectures', views.lectures, name='lectures'),
	path(r'register', views.register, name='register'),
	path(r'enter', views.enter, name='enter'),
	path(r'about', views.about, name='about'),
	path(r'add_lecture', views.add_lecture, name='add_lecture'),
	path(r'new_student', views.new_student, name='add_student'),
	path(r'lecture/<int:pk>/', views.lecture_detail, name='lecture_detail'),
	path(r'attendance', views.attendance, name='attendance'),
]