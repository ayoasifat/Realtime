# Generated by Django 4.1.4 on 2023-02-15 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_payments_options_alter_customusermodel_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusermodel',
            name='wallet',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
