from django.db import models


class Services(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.title


class Specialists(models.Model):
    name = models.CharField(max_length=100)
    services = models.ManyToManyField(Services, related_name='specialists')

    def __str__(self):
        return self.name


class Schedule(models.Model):
    specialists = models.ForeignKey(Specialists, on_delete=models.CASCADE, related_name='schedules')
    services = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    time = models.TimeField()


class Appointment(models.Model):
    customer = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=100)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='appointments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer
