# Generated by Django 4.2.7 on 2023-11-29 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruddecApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposits',
            name='status',
            field=models.CharField(choices=[('Successful', '1'), ('Failed', '3'), ('Pending', '2')], default='2', max_length=20),
        ),
    ]