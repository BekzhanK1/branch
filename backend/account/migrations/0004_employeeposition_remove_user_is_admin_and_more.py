# Generated by Django 4.2.7 on 2024-01-22 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_remove_companyemployee_company_and_more'),
        ('account', '0003_alter_user_is_active_alter_user_is_admin_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeePosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('shortname', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_employee',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_superadmin',
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('owner', 'Owner'), ('employee', 'Employee'), ('customer', 'Customer'), ('admin', 'Administrator')], default='employee', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='phonenumber',
            field=models.CharField(max_length=25),
        ),
        migrations.CreateModel(
            name='EmployeeUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.FloatField(blank=True, null=True)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.employeeposition')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_type', models.CharField(choices=[('new', 'New'), ('member', 'Member'), ('active_customer', 'Active Customer')], default='new', max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]