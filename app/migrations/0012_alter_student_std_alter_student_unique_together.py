# Generated by Django 4.2.2 on 2023-06-16 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_student_unique_identity_alter_student_std'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='std',
            field=models.CharField(choices=[('10', '10'), ('9', '9'), ('12', '12'), ('11', '11')], default='10', max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='student',
            unique_together={('roll_no', 'std')},
        ),
    ]
