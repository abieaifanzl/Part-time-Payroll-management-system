from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('userlogin/', views.userlogin, name='userlogin'),


    path('EmployeeHome/', views.userhome, name='userhome'),
    path('Payslip/', views.userpayslip, name='userpayslip'),

    path('ProfileSetting/', views.userprofilesetting, name='userprofilesetting'),
    path('update_profile/', views.update_profile, name='update_profile'),
    

    path('PayrollHistory/', views.userpayrollhistory, name='userpayrollhistory'),
    path('userhistory/', views.userhistory, name='userhistory'),




    path('HRhome/', views.hrhome, name='hrhome'),

    path('HRmanageEmployee/', views.hrmanageemployee, name='hrmanageemployee'),
    path('delete_parttime/<pt_id>/HRmanageEmployee/', views.delete_parttime, name='delete_parttime'),
    path('add_parttime/HRmanageEmployee/', views.add_parttime, name='add_parttime'),

    path('HRgeneratePayroll/', views.hrgeneratepayroll, name='hrgeneratepayroll'),
    path('HRpayroll/', views.hrpayroll, name='hrpayroll'),
    
    path('HRpayrollReport/', views.hrpayrollreport, name='hrpayrollreport'),
    path('HRpayrollReport/report/', views.hrreport, name='hrreport'),
    

]