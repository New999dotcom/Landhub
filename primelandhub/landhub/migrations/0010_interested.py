# Generated by Django 5.1.5 on 2025-02-04 06:52

import builtins
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landhub', '0009_remove_property_interseted'),
    ]

    operations = [
        migrations.CreateModel(
            name='interested',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interested', models.BooleanField(default=False)),
                ('message', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(default=builtins.pow)),
                ('propertyuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landhub.property')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landhub.reg_form')),
            ],
        ),
    ]
