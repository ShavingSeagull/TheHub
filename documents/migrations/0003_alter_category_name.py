# Generated by Django 3.2 on 2022-03-29 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20220329_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=40),
        ),
    ]
