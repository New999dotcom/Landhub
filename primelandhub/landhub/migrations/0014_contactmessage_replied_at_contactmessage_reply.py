# Generated by Django 5.1.5 on 2025-02-07 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landhub', '0013_contactmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='replied_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='reply',
            field=models.TextField(blank=True, null=True),
        ),
    ]
