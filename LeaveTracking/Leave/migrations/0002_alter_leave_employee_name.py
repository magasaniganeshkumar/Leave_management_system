# Generated by Django 3.2 on 2023-06-26 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Leave', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='Employee_Name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='empname', to='Leave.employee_detail'),
        ),
    ]
