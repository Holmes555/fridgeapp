# Generated by Django 2.1.5 on 2019-05-11 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sunflower', '0003_auto_20190511_2227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='measure',
            new_name='measure_test',
        ),
    ]
