from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import timezone
from .models import Staff, Attendance,Event
from django.db.models import Sum
from datetime import datetime
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib.auth import authenticate, login, logout


def home(request):
    query = request.GET.get("search", "").strip()
    total_salary = Staff.objects.aggregate(
    total=Sum("salary")
)["total"] or 0

    if query:
        staffs = Staff.objects.filter(
            Q(name__icontains=query) |
            Q(mobile__icontains=query)
        )
    else:
        staffs = Staff.objects.all()

    total_staff = Staff.objects.count()

    today = timezone.now().date()

    present_today = Attendance.objects.filter(
        date=today,
        status="Present"
    ).count()

    absent_today = Attendance.objects.filter(
        date=today,
        status="Absent"
    ).count()

    return render(request, "index.html", {
        "staffs": staffs,
        "query": query,
        "total_staff": total_staff,
        "present_today": present_today,
        "absent_today": absent_today,
        "total_salary": total_salary,
    })


def add_staff(request):
    if request.method == "POST":
        Staff.objects.create(
            name=request.POST["name"],
            mobile=request.POST["mobile"],
            address=request.POST["address"],
            salary=request.POST["salary"],
        )
    return redirect("home")


def edit_staff(request, id):
    staff = Staff.objects.get(id=id)

    if request.method == "POST":
        staff.name = request.POST["name"]
        staff.mobile = request.POST["mobile"]
        staff.address = request.POST["address"]
        staff.salary = request.POST["salary"]
        staff.save()
        return redirect("home")

    return render(request, "edit.html", {"staff": staff})


def delete_staff(request, id):
    Staff.objects.get(id=id).delete()
    return redirect("home")


def attendance(request):
    if request.method == "POST":

        staff_id = request.POST.get("staff")
        date = request.POST.get("date")
        status = request.POST.get("status")

        selected_date = datetime.strptime(date, "%Y-%m-%d").date()

        if selected_date > timezone.now().date():
            return redirect("attendance")

        attendance = Attendance.objects.filter(
            staff_id=staff_id,
            date=date
        ).first()

        if attendance:
            attendance.status = status
            attendance.save()
        else:
            Attendance.objects.create(
                staff_id=staff_id,
                date=date,
                status=status
            )

        return redirect("attendance")

    staffs = Staff.objects.all()
    attendance_list = Attendance.objects.select_related("staff").order_by("-date")

    return render(request, "attendance.html", {
        "staffs": staffs,
        "attendance_list": attendance_list,
    })
def salary_report(request):
    staffs = Staff.objects.all()
    report = []

    month = request.GET.get("month")

    for staff in staffs:

        attendance = Attendance.objects.filter(staff=staff)

        if month:
            year, mon = month.split("-")
            attendance = attendance.filter(
                date__year=year,
                date__month=mon
            )

        present_days = attendance.filter(status="Present").count()
        absent_days = attendance.filter(status="Absent").count()

        daily_salary = float(staff.salary) / 30
        payable_salary = round(daily_salary * present_days, 2)

        report.append({
            "staff": staff,
            "present": present_days,
            "absent": absent_days,
            "payable": payable_salary,
        })

    return render(request, "salary.html", {
        "report": report,
        "selected_month": month,
    })
def salary_pdf(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="salary_report.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, 800, "Salary Report")

    y = 760

    staffs = Staff.objects.all()

    for staff in staffs:

        present = Attendance.objects.filter(
            staff=staff,
            status="Present"
        ).count()

        absent = Attendance.objects.filter(
            staff=staff,
            status="Absent"
        ).count()

        salary = round((float(staff.salary) / 30) * present, 2)

        p.setFont("Helvetica", 11)

        p.drawString(50, y, f"Name : {staff.name}")
        p.drawString(220, y, f"Present : {present}")
        p.drawString(340, y, f"Absent : {absent}")
        p.drawString(450, y, f"Salary : ₹{salary}")

        y -= 25

        if y < 50:
            p.showPage()
            y = 800

    p.save()

    return response
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("home")

        return render(request, "login.html", {
            "error": "Invalid Username or Password"
        })

    return render(request, "login.html")


def logout_page(request):
    logout(request)
    return redirect("login")


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return redirect("home")
