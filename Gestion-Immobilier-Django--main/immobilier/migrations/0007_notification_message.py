# Generated by Django 5.0.5 on 2025-05-25 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('immobilier', '0006_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
