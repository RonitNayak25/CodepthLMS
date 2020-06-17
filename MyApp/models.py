from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, is_active=True, is_staff=False, is_admin=False, is_student=False, is_warden=False, is_mentor=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        if not full_name:
            raise ValueError('Users must have a full name')
        user = self.model(email=self.normalize_email(email), full_name=full_name)
        user.set_password(password)  # change user password
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin
        user.is_student = is_student
        user.is_warden = is_warden
        user.is_mentor = is_mentor
        user.save(using=self._db)
        return user

    def create_staffuser(self, full_name, email, password):
        user = self.create_user(email, full_name, password=password, )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password):
        user = self.create_user(email, full_name, password=password)
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=200, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)  # superuser
    is_student = models.BooleanField(default=False)
    is_warden = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # username
    # email and password are required by default
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mentor = models.ForeignKey('Mentor', on_delete=models.CASCADE, default=None)
    warden = models.ForeignKey('Warden', on_delete=models.CASCADE, default=None)
    parent_email = models.EmailField()

    def __str__(self):
        return str(self.user)


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    def get_full_name(self):
        return self.user.full_name


class Warden(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    def get_full_name(self):
        return self.user.full_name


class Leave(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    why_leave = models.TextField()
    comment = models.TextField(blank=True, null=True)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=True)

    def __str__(self):
        return f"application from {self.student.user.full_name} to his mentor"
