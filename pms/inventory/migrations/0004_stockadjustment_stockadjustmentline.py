# Generated by Django 3.0.6 on 2020-06-07 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_image'),
        ('inventory', '0003_auto_20200530_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockAdjustment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField()),
                ('reason', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StockAdjustmentLine',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('lot_number', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Drug')),
                ('stock_adjustment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.StockAdjustment')),
            ],
        ),
    ]
