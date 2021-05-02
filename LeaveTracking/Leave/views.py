from django.shortcuts import render, HttpResponse, redirect
from .models import Employee_Detail,Leave
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count,Sum

from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, View
from .serializer import EmployeeSerializer, LeaveSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, HttpResponse, get_object_or_404


# Create your views here.

SickLeave = 12
CasualLeave = 12
PersonalLeave = 12
Total = 36
YearRmainingLeaves = 0
#monthRemainingLeaves = 0


def Total_RemainingLeaves(request):
    if request.session.get("Employee_Id"):
        request.session.get("Employee_Id")
        sid = request.session.get("Employee_Id")
        emp = Employee_Detail.objects.get(id=sid)
        print(emp)
        Usedleaves = emp.empname.aggregate(Count('Leave_Type'))
        year = 2021
        print(Usedleaves)
        g = Usedleaves.get('Leave_Type__count')
        print(g)
        global  Total
        global  YearRmainingLeaves
        YearRmainingLeaves = Total-g
        return render(request,'Leave/Leanvecont.html',{'Total':Total,'Usedleaves': g,'YearRmainingLeaves': YearRmainingLeaves,'year': year,})
    else:
        messages.error(request, ("login to see Rmaingleaves in year 2021  !"))
        return redirect('home')


def createleave(request):
    if request.method == "POST":
        request.session.get("Employee_Id")
        sid = request.session.get("Employee_Id")
        emp = Employee_Detail.objects.get(id=sid)
        print(emp)
        levcon = Leave.objects.aggregate(Count('Leave_Type'))
        print(levcon)
        name = emp
        leave = request.POST['leave']
        year = 2021
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        reason = request.POST['reason']
        sta = request.POST['Pending']

        month = request.POST['month']
        if emp.empname.filter(Leave_Type=leave,Month=month):

            messages.success(request, ("you are alreay used in this",month , leave ))
            return redirect('createleave')
        if emp.empname.filter(Start_Date=startdate,End_Date=enddate):
            messages.success(request,("you are alreay used in this",startdate,))
            return redirect('createleave')

        try:
            lea = Leave.objects.create(Employee_Name=name, Leave_Type=leave, Month=month, Year=year,
                                       Start_Date=startdate, End_Date=enddate, Reason=reason, Status=sta).save()
            levcon = Leave.objects.aggregate(Count('Leave_Type'))
            print(levcon)
            messages.success(request, ("leave  appliyed successful.. !"))
            return redirect('home')
        except:
            messages.success(request, ("leave not  appliyed successful.. please try sometime!"))
            return redirect('home')
    elif request.method == "GET":
        if request.session.get("Employee_Id"):
            sid = request.session.get("Employee_Id")
            emp = Employee_Detail.objects.get(id=sid)
            print(emp)
            Usedleaves = emp.empname.aggregate(Count('Leave_Type'))
            year = 2021
            print(Usedleaves)
            g = Usedleaves.get('Leave_Type__count')
            print(g)
            global Total
            global YearRmainingLeaves
            YearRmainingLeaves = Total - g

            if Total <= g:
                messages.error(request, ("you did use all leaves in this year !"))
                return redirect('home')
            return render(request, "Leave/createleave.html")
        else:
            if request.session.get("Employee_Id"):
                return render(request, "Leave/createleave.html")
            else:
                messages.error(request, ("login to create leave!"))
                return redirect('home')




def Home(request):

    name = "WELCOME TO HOME"
    return render(request, "Leave/index.html", {'name': name})

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
def all_emp(request):
    if request.user.is_authenticated:
        emp = Employee_Detail.objects.all().order_by('-id')
        paginator = Paginator(emp,5)
        page = request.GET.get('pg')
        emp = paginator.get_page(page)
        return render(request, "Leave/allemp.html",{'emp':emp})
    else:
        messages.error(request, ("Viwing Employees not allowed Admin can only view all employeelist!!!!."))
        return redirect('home')


def delete_emp(request,task_id):
    emp =  Employee_Detail.objects.get(pk=task_id)
    emp.delete()
    messages.error(request,("Employee was deleted !!!!."))
    return redirect('home')

def Update_emp(request,task_id):
    if request.method == "POST":
        emp = Employee_Detail.objects.get(pk=task_id)
        emp.Employee_Name = request.POST['name']
        emp.password = request.POST['password']
        emp.Primary_Phone = request.POST['number']
        emp.Email = request.POST['email']
        emp.save()
        messages.success(request, ("Employee Updateded  successful.. !"))
        return redirect('home')
    elif request.method == "GET":
        emp = Employee_Detail.objects.get(pk=task_id)
        print(emp.Email)
        return render(request, "Leave/empupdate.html",{'emp':emp})

def pendinglist(request):

    if request.session.get("Employee_Id"):
        sid = request.session.get("Employee_Id")
        emp = Employee_Detail.objects.get(id=sid)
        print(emp)
        lev = emp.empname.filter(Status__exact='Pending')
        return render(request, "Leave/pendding.html", {'lev': lev})
    elif request.user.is_authenticated:
        lev = Leave.objects.filter(Status__exact='Pending')
        return render(request,"Leave/pendding.html",{'lev':lev})
    else:
        messages.error(request, ("login to see pendding status  !"))
        return redirect('home')


def canceledlist(request):
    if request.session.get("Employee_Id"):
        sid = request.session.get("Employee_Id")
        emp = Employee_Detail.objects.get(id=sid)
        print(emp)
        lev = emp.empname.filter(Status__exact='Canceled')
        return render(request, "Leave/canceledlist.html", {'lev': lev})
    elif request.user.is_authenticated:
        lev = Leave.objects.filter(Status__exact='Canceled')
        return render(request,"Leave/canceledlist.html",{'lev':lev})
    else:
        messages.error(request, ("login to see canceled status  !"))
        return redirect('home')

def Acceptedlist(request):
    if request.session.get("Employee_Id"):
        sid = request.session.get("Employee_Id")
        emp = Employee_Detail.objects.get(id=sid)
        print(emp)
        lev = emp.empname.filter(Status__exact='Accepted')
        return render(request, "Leave/pendding.html", {'lev': lev})
    elif request.user.is_authenticated:
        lev = Leave.objects.filter(Status__exact='Accepted')
        return render(request,"Leave/pendding.html",{'lev':lev})
    else:
        messages.error(request, ("login to see Accepted status  !"))
        return redirect('home')

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        psw = request.POST['password']
        phone = request.POST['number']
        email = request.POST['email']
        user = Employee_Detail.objects.create(Employee_Name=name,password=psw,Primary_Phone=phone,Email=email).save()
        messages.success(request, ("Register successful.. !"))
        return redirect('home')

    return render(request, "Leave/addemp.html")




def login(request):
    if request.method == "POST":
        name = request.POST['name']
        psw = request.POST['password']
        try:
            user = Employee_Detail.objects.get(Employee_Name=name,password=psw)
            #print(user.Employee_Name)
            request.session['Employee_Name'] = user.Employee_Name
            request.session['Employee_Id'] = user.id
            request.session['Employee_Email'] = user.Email
            messages.success(request, ("login successful.. !"))
            return redirect('home')
        except:
            messages.warning(request, ("employee not avalable.. !"))
            return redirect('home')
    return render(request,"Leave/login.html")

def logout(request):
    request.session.flush()
    messages.success(request, ("Logout successful.. !"))
    return redirect('home')






class EmployeeApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, **kwargs):
        if kwargs.get('pk'):
            pk = kwargs.get('pk')
            saved_employee = get_object_or_404(Employee_Detail.objects.all(), pk=pk)
            serializer = EmployeeSerializer(saved_employee)
            return Response({"Employee_Detail": serializer.data})

        employees = Employee_Detail.objects.all()
        employee = EmployeeSerializer(employees, many=True)
        return Response({'Employee_Detail': employee.data})


    def post(self, request):

        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        employee = get_object_or_404(Employee_Detail.objects.all(), pk=pk)
        serializer = EmployeeSerializer(instance=employee, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            employee_saved = serializer.save()
        return Response({"success": "Article '{}' updated successfully".format(employee.Employee_Name)})

    def delete(self, request, pk):
        employee = get_object_or_404(Employee_Detail.objects.all(), pk=pk)
        employee.delete()
        return Response({"message": "Article with id `{}` has been deleted.".format(pk)}, status=204)



class LeaveApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, **kwargs):
        if kwargs.get('pk'):
            pk = kwargs.get('pk')
            saved_leave = get_object_or_404(Leave.objects.all(), pk=pk)
            serializer = LeaveSerializer(saved_leave)
            return Response({"Leave": serializer.data})

        leaves = Leave.objects.all()
        leave = LeaveSerializer(leaves, many=True)
        return Response({'Leave': leave.data})


    def post(self, request):

        serializer = LeaveSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        leavee = get_object_or_404(Leave.objects.all(), pk=pk)
        serializer = LeaveSerializer(instance=leavee, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            leavee_saved = serializer.save()
        return Response({"success": "Article '{}' updated successfully".format(leavee.Employee_Name)})

    def delete(self, request, pk):
        leave = get_object_or_404(Leave.objects.all(), pk=pk)
        leave.delete()
        return Response({"message": "Article with id `{}` has been deleted.".format(pk)}, status=204)


def handler404(request,*args,**kwargs):
    messages.error(request, ("Your enter url request Not Available in this Application.Please send Valid Request   !"))
    return redirect('home')


