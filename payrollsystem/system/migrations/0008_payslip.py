# Generated by Django 5.0 on 2024-10-10 14:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_delete_payslip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payslip',
            fields=[
                ('PAYSLIPid', models.AutoField(primary_key=True, serialize=False)),
                ('PAYSLIPrecipient', models.CharField(max_length=50)),
                ('PAYSLIPpayperiodstart', models.CharField(max_length=50)),
                ('PAYSLIPpayperiodend', models.CharField(max_length=50)),
                ('PAYSLIPweekdaywh', models.CharField(max_length=50)),
                ('PAYSLIPweekdaybr', models.CharField(max_length=50)),
                ('PAYSLIPweekdaysalary', models.CharField(max_length=50)),
                ('PAYSLIPweekendwh', models.CharField(max_length=50)),
                ('PAYSLIPweekendbr', models.CharField(max_length=50)),
                ('PAYSLIPweekendsalary', models.CharField(max_length=50)),
                ('PAYSLIPtotalworkhour', models.CharField(max_length=5)),
                ('PAYSLIPtotalbreakhour', models.CharField(max_length=5)),
                ('PAYSLIPtotalsalary', models.CharField(max_length=50)),
                ('PTid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.parttime')),
            ],
        ),
    ]
