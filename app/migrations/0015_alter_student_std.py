# Generated by Django 4.2.2 on 2023-06-16 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_student_std_alter_student_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='std',
            field=models.CharField(choices=[('12', '12'), ('10', '10'), ('11', '11'), ('9', '9')], default='10', max_length=50),
        ),
    ]
