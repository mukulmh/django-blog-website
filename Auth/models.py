from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccoutManager(BaseUserManager):
    def create_user(self, phone, username, email, password=None):
        if not phone:
            raise ValueError("User must have a phone no.")
        if not username:
            raise ValueError("User must have an username.")
        if not email:
            raise ValueError("User must have an email.")

        user = self.model(
            phone = phone,
            username = username,
            email = email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, email, password):
        user = self.create_user(
            phone = phone,
            username = username,
            email = email,
            password = password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    phone = models.CharField(verbose_name='phone', max_length=20, unique=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    image = models.ImageField(upload_to='pics', null=True)
    bio = models.TextField(max_length=255, null=True)
    date_joined = models.DateTimeField(verbose_name='date_joined',auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login',auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username','email']

    objects = MyAccoutManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True


class ResetCode(models.Model):
    code = models.CharField(max_length=8, unique=True, null=True)
    phone = models.ForeignKey(Account, to_field="phone", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
