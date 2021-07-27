from django.shortcuts import render, redirect	
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from django.http import HttpResponse
import datetime
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import registerForm
from django.shortcuts import get_object_or_404

def home(request):
	return render(request, 'home.html')

def signin(request):
	return render(request, 'login.html')

def logout(request):
	auth.logout(request)
	return redirect('/')

def enter(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages.info(request, 'Username or password is incorrect')

	context = {}
	return render(request, 'login.html', context)
	
def about(request):
	return render(request, 'about.html')
	
def register(request):
	context = {}

	if request.POST:
		form = registerForm(request.POST)
		if form.is_valid():
			account = form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			login(request, account, backend='django.contrib.auth.backends.ModelBackend')
			return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = registerForm()
		context['registration_form'] = form
	return render(request, 'register.html', context)

def dashboard(request):
	teacher = request.user
	Lect = teacher.lecture_set.all()
	sum = 0
	for x in Lect:
		sum = sum + 1
	date = datetime.datetime.now()
	return render(request, 'dashboard.html', {'sum': sum, 'date':date})

def lectures(request):
	teacher = request.user
	Lect = teacher.lecture_set.all()
	date = datetime.datetime.now()
	return render(request, 'lectures.html', {'Lect': Lect, 'date':date})

def add_lecture(request):
	if request.method == 'POST':
		name = request.POST['name']
		date = datetime.datetime.now()
		teacher = request.user           # TO save the current user
		lect = Lecture(name=name, date=date, teacher=teacher)
		lect.save()
		return render(request, 'attendance.html',{'lecture':lect,'student':Student.objects.all()})
	return render(request, 'add_lectures.html')

def new_student(request):
	if request.method == 'POST':
		name = request.POST['name']
		roll_no = request.POST['roll_no']
		student = Student(name = name, roll_no=roll_no)
		student.save()
	Stu = Student.objects.all()
	return render(request, 'students.html', {'Stu':Stu})

def lecture_detail(request, pk):
	student = Student.objects.all()
	lecture = Lecture.objects.get(pk = pk)    
	attend = lecture.status_set.all()
	context = {'student': student, 'lecture': lecture, 'attend': attend}
	return render(request, 'detail.html', context)

def attendance(request):
	student_id_list = request.POST.getlist('status')
	lecture_id = request.POST['lecture_id']

	student_list = list(Student.objects.all().values_list('id',flat=True))

	for student in student_list:
		obj = Status(student_id = student, lecture_id = int(lecture_id))
		if str(student) in student_id_list:
			obj.status = True
		else:
			obj.status = False
		obj.save()

	return redirect('lectures')