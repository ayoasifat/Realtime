# Generated by Django 4.1.4 on 2023-03-15 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_conversation_timestamp_alter_message_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='picture',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos/'),
        ),
    ]
