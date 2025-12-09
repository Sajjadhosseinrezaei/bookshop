from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from utils.models import TimeStampedModel




class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom User model with email as the unique identifier
    """
    email = models.EmailField(max_length=255, unique=True, verbose_name='ایمیل')
    first_name = models.CharField(max_length=100, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=100, blank=True, verbose_name='نام خانوادگی')
    image = models.ImageField(upload_to='users/', blank=True, null=True, verbose_name='تصویر')
    
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_staff = models.BooleanField(default=False, verbose_name='کارمند')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email is already required by default
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        ordering = ['-created']
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between
        """
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name if full_name else self.email
    
    def get_short_name(self):
        """
        Return the short name for the user
        """
        return self.first_name if self.first_name else self.email




# models.py
class Address(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    
    title = models.CharField("عنوان آدرس", max_length=100, blank=True)  # خانه، محل کار
    recipient_name = models.CharField("نام گیرنده", max_length=100)
    recipient_phone = models.CharField("موبایل گیرنده", max_length=11)

    province = models.CharField("استان", max_length=50)
    city = models.CharField("شهر", max_length=50)
    street = models.TextField("آدرس کامل (خیابان، کوچه، پلاک، واحد و ...)")
    postal_code = models.CharField("کد پستی", max_length=10, blank=True)

    is_default = models.BooleanField("آدرس پیش‌فرض", default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.recipient_name} - {self.city}"

    class Meta:
        verbose_name_plural = "آدرس‌ها"