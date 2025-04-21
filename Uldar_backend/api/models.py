import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, age, password=None):
        if not email:
            raise ValueError('Users must have email address')
        if not username:
            raise ValueError('Users must have username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            age=age,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, first_name, last_name, age, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            age=age,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", unique=True)
    username = models.CharField(max_length=80, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=80)
    bio = models.TextField(blank=True, null=True, max_length=3000)
    age = models.DateField(default=datetime.date.today)
    avatar = models.ImageField(upload_to='image', blank=True, null=True, default='avatar.svg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'age']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app):
        return self.is_admin


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=300, blank=False)
    body = models.TextField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    code_field = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated', '-created']


class Message(models.Model):
    body = models.TextField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    is_best_answer = models.BooleanField(default=False)
    code_field = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[:40]

    class Meta:
        ordering = ['-updated', '-created']
