from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Login
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Staff
    path('add/', views.add_staff, name='add_staff'),
    path('edit/<int:id>/', views.edit_staff, name='edit_staff'),
    path('delete/<int:id>/', views.delete_staff, name='delete_staff'),

    # Attendance
    path('attendance/', views.attendance, name='attendance'),
    

    # Salary
    path('salary/', views.salary_report, name='salary'),
    path('salary-pdf/', views.salary_pdf, name='salary_pdf'),
]