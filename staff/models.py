from django.db import models
from django.utils import timezone

class Staff(models.Model):
   
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

   

class Attendance(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=[
            ('Present', 'Present'),
            ('Absent', 'Absent')
        ],
        default='Present'
    )

    def __str__(self):
        return f"{self.staff.name} - {self.date}"
    class Meta:
     unique_together = ('staff', 'date')
         

class Event(models.Model):
    client_name = models.CharField(max_length=100)
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()
    event_time = models.TimeField()
    location = models.CharField(max_length=200)
    required_staff = models.PositiveIntegerField()
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Upcoming", "Upcoming"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
        default="Upcoming"
    )

    def __str__(self):
        return f"{self.client_name} - {self.event_name}"