# Generated by Django 5.1.5 on 2025-03-17 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landhub', '0026_remove_chat_receiver_remove_chat_sender_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Chat',
        ),
    ]
