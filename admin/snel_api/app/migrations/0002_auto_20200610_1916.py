# Generated by Django 3.0.6 on 2020-06-10 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilisateur',
            name='login',
        ),
        migrations.DeleteModel(
            name='Administrateur',
        ),
    ]
