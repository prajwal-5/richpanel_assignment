# Generated by Django 4.0.6 on 2022-08-04 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0002_alter_user_plan_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='plan_type',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assignment.plan'),
        ),
    ]
