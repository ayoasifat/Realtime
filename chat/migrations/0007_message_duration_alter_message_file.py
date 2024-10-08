# Generated by Django 4.1.4 on 2023-04-16 17:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_alter_message_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='duration',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3'])]),
        ),
    ]
