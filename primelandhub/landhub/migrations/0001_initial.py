# Generated by Django 5.1.4 on 2025-01-08 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='reg_form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('pwd', models.CharField(max_length=30)),
                ('confirmpwd', models.CharField(max_length=30)),
                ('age', models.IntegerField(max_length=3)),
                ('phone', models.IntegerField(max_length=10)),
                ('place', models.CharField(max_length=200)),
                ('gend', models.CharField(blank=True, choices=[('male', 'MALE'), ('female', 'FEMALE')], max_length=10, null=True)),
            ],
        ),
    ]
