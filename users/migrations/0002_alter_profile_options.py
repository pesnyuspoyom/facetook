# Generated by Django 4.1.5 on 2023-02-01 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Профайл', 'verbose_name_plural': 'Профайлы'},
        ),
    ]
