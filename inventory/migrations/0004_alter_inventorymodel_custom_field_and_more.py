# Generated by Django 4.1.1 on 2022-11-26 20:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_inventorymodel_custom_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorymodel',
            name='custom_field',
            field=models.JSONField(max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='inventorymodel',
            name='qr_key',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.AlterField(
            model_name='inventorymodel',
            name='serial_number',
            field=models.CharField(max_length=256, null=True),
        ),
    ]