# Generated by Django 4.2.7 on 2024-01-22 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0006_alter_company_company_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyemployee',
            name='company',
        ),
        migrations.RemoveField(
            model_name='companyemployee',
            name='employee',
        ),
        migrations.AlterField(
            model_name='company',
            name='company_owner',
            field=models.ForeignKey(default=63, on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL),
        ),
    ]