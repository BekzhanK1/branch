# Generated by Django 4.2.7 on 2024-01-29 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_rename_item_orderitem_menu_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='menu_item',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]