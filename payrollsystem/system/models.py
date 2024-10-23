from django.db import models

# Create your models here.
class Parttime(models.Model):
    PTid = models.CharField(primary_key=True,max_length=5)
    PTname = models.CharField(max_length=50)
    PTpassword = models.CharField(null=True,max_length=50)
    PTphonenumber = models.CharField(null=True,max_length=50)
    PTbankacc = models.CharField(null=True,max_length=50)
    PTic = models.CharField(null=True,max_length=50)

class Hr(models.Model):
    HRid = models.CharField(primary_key=True,max_length=5)
    HRname = models.CharField(max_length=50)
    HRpassword = models.CharField(max_length=50)

class Payslip(models.Model):
    PAYSLIPid = models.AutoField(primary_key=True)
    PTid = models.ForeignKey(Parttime, on_delete=models.CASCADE)
    PAYSLIPrecipient = models.CharField(max_length=50)
    PAYSLIPpayperiodstart = models.CharField(max_length=50)
    PAYSLIPpayperiodend = models.CharField(max_length=50)
    PAYSLIPweekdaywh = models.CharField(max_length=50)
    PAYSLIPweekdaybr = models.CharField(max_length=50)
    PAYSLIPweekdaysalary = models.CharField(max_length=50)
    PAYSLIPweekendwh = models.CharField(max_length=50)
    PAYSLIPweekendbr = models.CharField(max_length=50)
    PAYSLIPweekendsalary = models.CharField(max_length=50)
    PAYSLIPtotalworkhour = models.CharField(max_length=5)
    PAYSLIPtotalbreakhour = models.CharField(max_length=5)
    PAYSLIPtotalsalary = models.CharField(max_length=50)








