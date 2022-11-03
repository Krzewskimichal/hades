# Generated by Django 4.1.1 on 2022-11-03 01:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorymodel',
            name='qr_key',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
