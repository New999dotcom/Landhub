# Generated by Django 5.1.5 on 2025-03-10 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landhub', '0021_buyer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyer',
            name='confirmpwd',
        ),
        migrations.AlterField(
            model_name='buyer',
            name='pwd',
            field=models.CharField(max_length=128),
        ),
    ]
