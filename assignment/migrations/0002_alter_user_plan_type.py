# Generated by Django 4.0.6 on 2022-08-04 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='plan_type',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='assignment.plan'),
        ),
    ]