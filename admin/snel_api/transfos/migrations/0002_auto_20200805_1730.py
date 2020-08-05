# Generated by Django 3.0.6 on 2020-08-05 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transformateur',
            name='phase1_state',
            field=models.CharField(choices=[('OFF', 'Eteint'), ('ON', 'Allumé')], default='OFF', max_length=10),
        ),
        migrations.AddField(
            model_name='transformateur',
            name='phase2_state',
            field=models.CharField(choices=[('OFF', 'Eteint'), ('ON', 'Allumé')], default='OFF', max_length=10),
        ),
        migrations.AddField(
            model_name='transformateur',
            name='phase3_state',
            field=models.CharField(choices=[('OFF', 'Eteint'), ('ON', 'Allumé')], default='OFF', max_length=10),
        ),
    ]
