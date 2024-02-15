# Generated by Django 4.1.12 on 2024-02-15 06:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(choices=[('audusd', 'AUDUSD'), ('btcusd', 'BTCUSD'), ('ethusd', 'ETHUSD'), ('euraud', 'EURAUD'), ('eurgbp', 'EURGBP'), ('gbpusd', 'GBPUSD'), ('jpyusd', 'JPYUSD'), ('nzdusd', 'NZDUSD'), ('xauusd', 'XAUUSD')], default='xauusd', max_length=15)),
                ('amount', models.CharField(max_length=15)),
                ('profit', models.CharField(blank=True, max_length=15)),
                ('type', models.CharField(choices=[('buy', 'BUY'), ('sell', 'SELL')], default='buy', max_length=7)),
                ('lot_size', models.CharField(max_length=15)),
                ('duration', models.TimeField()),
                ('status', models.CharField(choices=[('open', 'OPEN'), ('closed', 'CLOSED')], default='open', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]