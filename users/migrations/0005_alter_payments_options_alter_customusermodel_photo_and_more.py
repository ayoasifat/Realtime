# Generated by Django 4.1.4 on 2023-02-15 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_payments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payments',
            options={'verbose_name_plural': 'Payments'},
        ),
        migrations.AlterField(
            model_name='customusermodel',
            name='photo',
            field=models.ImageField(blank=True, default=None, upload_to='profile pictures/'),
        ),
        migrations.AlterField(
            model_name='customusermodel',
            name='status',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]