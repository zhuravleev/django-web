from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    history = HistoricalRecords()
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return f'{self.first_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Car(models.Model):
    model = models.CharField(verbose_name='Модель машины', max_length=255)
    number = models.CharField(verbose_name='Гос. номер', max_length=10)

    history = HistoricalRecords()

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'


class Driver(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    middle_name = models.CharField(verbose_name='Отчество', max_length=255, blank=True)
    photo = models.ImageField(verbose_name='Фото', upload_to='img/drivers')

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


    class Meta:
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'


class Order(models.Model):
    customer = models.ForeignKey(User, verbose_name='Заказчик', on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, verbose_name='Водитель', on_delete=models.CASCADE)
    car = models.ForeignKey(Car, verbose_name='Машина', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now=False, auto_now_add=True)

    STATUS_CHOICES = (('CANCELED', 'Отменён'), ('ACTIVE', 'Активен'), ('DONE', 'Завершён'))
    status = models.CharField(verbose_name='Статус', choices=STATUS_CHOICES, default='ACTIVE', max_length=8)

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.id} - {self.status}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
