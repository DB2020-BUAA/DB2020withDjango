# Generated by Django 3.1.3 on 2020-12-19 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_update_imgs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
