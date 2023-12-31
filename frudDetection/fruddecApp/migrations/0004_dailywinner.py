# Generated by Django 4.2.7 on 2023-12-31 09:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fruddecApp', '0003_deposits_comment_alter_deposits_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyWinner',
            fields=[
                ('winner_id', models.AutoField(primary_key=True, serialize=False)),
                ('winning_date', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=2, default=100.0, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
