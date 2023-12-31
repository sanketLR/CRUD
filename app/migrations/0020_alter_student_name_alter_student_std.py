# Generated by Django 4.2.1 on 2023-06-22 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_student_options_alter_student_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cust_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='student',
            name='std',
            field=models.CharField(choices=[('12', '12'), ('9', '9'), ('10', '10'), ('11', '11')], default='10', max_length=50),
        ),
    ]
