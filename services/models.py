from django.db import models

class Salon(models.Model):
    address = models.CharField(max_length=100,verbose_name='Адрес')
    phone = models.CharField(max_length=100,verbose_name='Телефон')

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Салон'
        verbose_name_plural = 'Салоны'

class Service(models.Model):
    title = models.CharField(max_length=100,verbose_name='Название улсуги')
    description = models.TextField(verbose_name='Описание услуги')
    price = models.DecimalField(decimal_places=2, max_digits=10,verbose_name='Цена услуги')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

class Specialist(models.Model):
    name = models.CharField(max_length=100,verbose_name='Имя специалиста')
    service = models.ManyToManyField(Service, related_name='specialists',verbose_name='Услуга')
    salon = models.ManyToManyField(Salon, related_name='specialists',verbose_name='Салон')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'


class Schedule(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='schedules',verbose_name='Специалист')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='schedules',verbose_name='Салон')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    is_available = models.BooleanField(default=True,verbose_name='Статус записи')

    def __str__(self):
        return f'{self.specialist.name, self.salon.address}'

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'


class Appointment(models.Model):
    customer = models.CharField(max_length=100,verbose_name='Имя заказчика')
    customer_phone = models.CharField(max_length=100,verbose_name='Телефон заказчика')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='appointments',verbose_name='Запись')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer


    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
