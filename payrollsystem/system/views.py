from django.shortcuts import render, redirect , get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q  
from system.models import Parttime, Payslip, Hr

# Create your views here.

# Login  Page

def login(request):
    return render(request, 'login.html')



def userlogin(request):
    if request.method == 'POST':
        userRole = request.POST['userRole']
        userName = request.POST['userName']
        userPassword = request.POST['userPassword']

        if userRole == 'HR':
            try:
                user = Hr.objects.get(HRname=userName, HRpassword=userPassword)
                request.session['User'] = user.HRid
                return redirect('hrhome')
            except Hr.DoesNotExist:
                return render(request, 'login.html', {'error': 'Invalid username or password'})
        
        else:  # Assuming this is for Parttime role
            try:
                user = Parttime.objects.get(PTname=userName, PTpassword=userPassword)
                request.session['User'] = user.PTid
                return redirect('userhome')
            except Parttime.DoesNotExist:  # Corrected here
                return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

    




# Employee Page

def userhome(request):

    if 'User' in request.session:
        pt_id = request.session['User']  
        pt_info = Parttime.objects.get(PTid=pt_id) 
        context = {
            'pt_info': pt_info
        }
        return render(request, 'userhome.html', context)  
    else:
        return redirect('login')
    


def userprofilesetting(request):

    if 'User' in request.session:
        pt_id = request.session['User']  
        pt_info = Parttime.objects.get(PTid=pt_id) 
        context = {
            'pt_info': pt_info
        }
        return render(request, 'userprofilesetting.html', context)  
    else:
        return redirect('login')
    


@require_POST
def update_profile(request):

    if 'User' in request.session:
        pt_id = request.session['User']  
        parttime = Parttime.objects.get(PTid=pt_id)
        # Update existing employee
        parttime.PTname = request.POST['UpdateName']
        parttime.PTpassword = request.POST['UpdatePassword']
        parttime.PTphonenumber = request.POST['UpdatePhoneNo']
        parttime.PTbankacc = request.POST['UpdateBankAcc']
        parttime.PTic = request.POST['UpdateIC'] 

        parttime.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('userprofilesetting') 
    else:
        return redirect('login')
    




def userpayslip(request):

    if 'User' in request.session:
        pt_id = request.session['User']
        
        # Fetch the latest payslip for the given PTid
        try:
            payslip_info = Payslip.objects.filter(PTid=pt_id).order_by('-PAYSLIPid').first()
            
            # If no payslip found, you might want to handle this case
            if payslip_info is None:
                context = {'error': 'No payslip found.'}
                return render(request, 'userpayslip.html', context)
            
            context = {
                'payslip_info': payslip_info
            }
            return render(request, 'userpayslip.html', context)  
        
        except Payslip.DoesNotExist:
            return render(request, 'userpayslip.html', {'error': 'Payslip not found.'})
    else:
        return redirect('login')
    






def userpayrollhistory(request):

    if 'User' in request.session:
        pt_id = request.session['User']  
        payslip_list = Payslip.objects.filter(PTid=pt_id) 
        context = {
            'payslip_list': payslip_list
        }
        return render(request, 'userpayrollhistory.html', context)  
    else:
        return redirect('login')
    

def userhistory(request):
    if 'User' in request.session:
        pt_id = request.session['User']
        date_start = request.GET.get('payperiodstart')
        
        # Fetch the latest payslip for the given PTid and pay period start date
        payslip_info = Payslip.objects.get(PTid=pt_id,PAYSLIPpayperiodstart=date_start)

        context = {
            'payslip_info': payslip_info
            }
        return render(request, 'userpayslip.html', context)
    
    else:
        return redirect('login')















# HR Page

def hrhome(request):

    if 'User' in request.session:
        hr_id = request.session['User']  
        hr_info = Hr.objects.get(HRid=hr_id) 
        context = {
            'hr_info': hr_info
        }
        return render(request, 'hrhome.html', context)  
    else:
        return redirect('login')



def hrmanageemployee(request):

    #fetch part-time name
    parttime_list = Parttime.objects.all()

    context = {
        'parttime_list': parttime_list,
    }

    return render(request, 'hrmanageemployee.html',context)



def delete_parttime(request, pt_id):
    # Only allow deletion via POST method for security reasons
    if request.method == 'POST':
        parttime = get_object_or_404(Parttime, PTid=pt_id)
        parttime.delete()
        return redirect(hrmanageemployee)
  
@require_POST
def add_parttime(request):
    employee_id = request.POST['AddEmployeeID']
    
    # Check if the employee already exists
    try:
        parttime = Parttime.objects.get(PTid=employee_id)
        # Update existing employee
        parttime.PTname = request.POST['AddEmployeeName']
        parttime.PTphonenumber = request.POST['AddEmployeePhoneNo']
        parttime.PTbankacc = request.POST['AddEmployeeBankAcc']
        parttime.PTic = request.POST['AddEmployeeIC']
        
    except Parttime.DoesNotExist:
        # Create a new employee if not exists
        parttime = Parttime(
            PTid=employee_id,
            PTname=request.POST['AddEmployeeName'],
            PTphonenumber=request.POST['AddEmployeePhoneNo'],
            PTbankacc=request.POST['AddEmployeeBankAcc'],
            PTic=request.POST['AddEmployeeIC'],
            PTpassword=request.POST['AddEmployeeName']  
        )

    parttime.save()
    return redirect('hrmanageemployee')
















def hrgeneratepayroll(request):
    #fetch part-time name
    parttime_list = Parttime.objects.all()

    context = {
        'parttime_list': parttime_list,
    }

    return render(request, 'hrgeneratepayroll.html', context)



def hrpayroll(request): 

    # Get staff name
    staffname = request.GET.get('staff_name')

    # Get part-time ID
    parttime = Parttime.objects.get(PTname=staffname)  # Fetch the part-time object
    staffid = parttime.PTid  # Get the part-time staff ID

    # Get pay period
    pay_period_start = request.GET.get('payperiod_start')
    pay_period_end = request.GET.get('payperiod_end')

    # Check if a payslip for this staff already exists within the given pay period
    existing_payslip = Payslip.objects.filter(
        PTid=parttime,
        PAYSLIPpayperiodstart=pay_period_start,
        PAYSLIPpayperiodend=pay_period_end
    ).exists()

    if existing_payslip:
        # Handle the case where a payslip already exists
        context = {
            'error_message': 'A payslip for this staff and pay period already exists.'
        }
        return render(request, 'hrgeneratepayroll.html', context)

    # Proceed with calculating and creating the new payslip if no conflict is found

    # Calculate weekday work hours
    wdwh1 = int(request.GET.get('work_hour1'))
    wdwh2 = int(request.GET.get('work_hour2'))
    wdwh3 = int(request.GET.get('work_hour3'))
    wdwh4 = int(request.GET.get('work_hour4'))
    wdwh5 = int(request.GET.get('work_hour5'))

    Totalweekdaywork = wdwh1 + wdwh2 + wdwh3 + wdwh4 + wdwh5

    # Calculate weekday break hours
    wdbr1 = int(request.GET.get('break_hour1'))
    wdbr2 = int(request.GET.get('break_hour2'))
    wdbr3 = int(request.GET.get('break_hour3'))
    wdbr4 = int(request.GET.get('break_hour4'))
    wdbr5 = int(request.GET.get('break_hour5'))

    Totalweekdaybreak = wdbr1 + wdbr2 + wdbr3 + wdbr4 + wdbr5

    # Calculate net weekday work hours and salary
    weekdaywork = Totalweekdaywork - Totalweekdaybreak
    weekdaysalary = weekdaywork * 8

    # Calculate weekend work hours
    wkwh1 = int(request.GET.get('work_hour6'))
    wkwh2 = int(request.GET.get('work_hour7'))

    Totalweekendwork = wkwh1 + wkwh2

    # Calculate weekend break hours
    wkbr1 = int(request.GET.get('break_hour6'))
    wkbr2 = int(request.GET.get('break_hour7'))

    Totalweekendbreak = wkbr1 + wkbr2

    # Calculate net weekend work hours and salary
    weekendwork = Totalweekendwork - Totalweekendbreak
    weekendsalary = weekendwork * 10

    # Total salary
    totalsalary = weekdaysalary + weekendsalary

    # Total work hour & break
    totalworkhour = weekendwork + weekdaywork
    totalbreakhour = Totalweekendbreak + Totalweekdaybreak

    # Save to Payslip model
    payslip = Payslip(
        PTid=parttime,  # Use the parttime object
        PAYSLIPrecipient=staffname, 
        PAYSLIPpayperiodstart=pay_period_start,
        PAYSLIPpayperiodend=pay_period_end,
        PAYSLIPweekdaywh=Totalweekdaywork,
        PAYSLIPweekdaybr=Totalweekdaybreak,
        PAYSLIPweekdaysalary=weekdaysalary,
        PAYSLIPweekendwh=Totalweekendwork,
        PAYSLIPweekendbr=Totalweekendbreak,
        PAYSLIPweekendsalary=weekendsalary,
        PAYSLIPtotalworkhour=totalworkhour,
        PAYSLIPtotalbreakhour=totalbreakhour,
        PAYSLIPtotalsalary=totalsalary
    )
    payslip.save()

    # Combine context into a single dictionary
    context = {
        'Totalweekdaywork': Totalweekdaywork,
        'Totalweekendwork': Totalweekendwork,
        'Totalweekdaybreak': Totalweekdaybreak,
        'Totalweekendbreak': Totalweekendbreak,
        'payperiodstart': pay_period_start,
        'payperiodend': pay_period_end,
        'staffname': staffname,
        'staffid': staffid,
        'weekdaysalary': weekdaysalary,
        'weekendsalary': weekendsalary,
        'totalsalary': totalsalary,
        'totalworkhour': totalworkhour,
        'totalbreakhour': totalbreakhour
    }

    return render(request, 'hrpayroll.html', context)





def hrpayrollreport(request):

    #fetch payroll period
    payslip_list = Payslip.objects.values('PAYSLIPpayperiodstart').distinct()

    context = {
        'payslip_list': payslip_list,
    }

    return render(request, 'hrpayrollreport.html', context)


def hrreport(request):

     # Get pay period
    startdate = request.GET.get('start_date')
    enddate = request.GET.get('end_date')


    payslip_thisdate = Payslip.objects.filter(PAYSLIPpayperiodstart=startdate)

    context = {
        'startdate': startdate,
        'enddate': enddate,
        'payslip_thisdate': payslip_thisdate,

    }

    return render(request, 'hrreport.html', context)






