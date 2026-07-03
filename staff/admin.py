from django.contrib import admin
from .models import Staff, Attendance
from .models import Staff, Attendance, Event

admin.site.register(Staff)
admin.site.register(Attendance)
admin.site.register(Event)
