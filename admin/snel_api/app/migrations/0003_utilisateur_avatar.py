# Generated by Django 3.0.6 on 2020-06-11 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200610_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='avatar',
            field=models.ImageField(default='medias/img/avatar.jpg', upload_to='medias/img/'),
        ),
    ]
