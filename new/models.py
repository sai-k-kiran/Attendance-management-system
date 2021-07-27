from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
import os
from django.utils import timezone

STATUS = (
    ('absent', 'Absent'),
    ('present', 'Present')
)

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password=None):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Teacher(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(verbose_name="email", max_length=60)
	username = models.CharField(max_length=30, unique=True)
	date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser= models.BooleanField(default=False)


	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

	def get_username(self):
		return self.username

	def get_absolute_url(self):
		return "/users/%i/" % (self.pk)

class Lecture(models.Model):
	name = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now_add=True)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True) #Do not use OneToOneField or
	                                                                                 #unique constraint error will rise
	class Meta:
		ordering = ['date']

	def __str__(self):
		return self.name

class Student(models.Model):
	name = models.CharField(max_length=200)
	roll_no = models.CharField(max_length=10, unique=True)

	class Meta:
		ordering = ['roll_no']
	
	def __str__(self):
		return self.name

class CustomBooleanField(models.BooleanField):

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return value #return Present/Absent

class Status(models.Model):
	lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, default='')
	student = models.ForeignKey(Student, on_delete=models.CASCADE, default='')
	status = models.BooleanField(default=False)
