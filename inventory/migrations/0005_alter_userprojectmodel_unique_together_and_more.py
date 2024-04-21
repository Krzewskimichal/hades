# Generated by Django 4.1.1 on 2022-12-11 22:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0004_alter_inventorymodel_custom_field_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userprojectmodel',
            unique_together={('user', 'project')},
        ),
        migrations.CreateModel(
            name='InventoryHistoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('what_happen', models.CharField(max_length=256)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('change_type', models.CharField(choices=[('CO', 'change owner'), ('CL', 'change localization'), ('CS', 'change status')], max_length=2)),
                ('inventory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.inventorymodel')),
            ],
        ),
    ]
