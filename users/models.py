from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# Email : Đúng định dạng email
# Password: 8 kí tự, có kí tự đặc biệt, kí tự đầu tiên viết hoa
# Username: # không trùng, k có space, không có kí tự đặc biệt


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
