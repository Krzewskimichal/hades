# Generated by Django 4.1.1 on 2022-11-03 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_inventorymodel_qr_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorymodel',
            name='custom_field',
            field=models.JSONField(default=None, max_length=2048),
            preserve_default=False,
        ),
    ]
