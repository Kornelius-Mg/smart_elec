# Generated by Django 3.0.6 on 2020-08-03 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200711_2204'),
        ('transfos', '0001_initial'),
        ('compteur', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(choices=[('Domestique', 'Domestique'), ('Semi-industriel', 'Semi-industriel'), ('Industriel', 'Industriel')], max_length=45)),
                ('p_max', models.FloatField()),
                ('q_max', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='balance',
            name='compteur',
        ),
        migrations.RemoveField(
            model_name='transfertcredit',
            name='destinataire',
        ),
        migrations.RemoveField(
            model_name='transfertcredit',
            name='expeditaire',
        ),
        migrations.RemoveField(
            model_name='compteur',
            name='active_class',
        ),
        migrations.AlterField(
            model_name='compteur',
            name='appartement',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Appartement'),
        ),
        migrations.AlterField(
            model_name='compteur',
            name='modele',
            field=models.IntegerField(choices=[('Monophasé', 'Monophasé'), ('Biphasé', 'Biphasé'), ('Triphasé', 'Triphasé')]),
        ),
        migrations.AlterField(
            model_name='compteur',
            name='transformateur',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transfos.Transformateur'),
        ),
        migrations.DeleteModel(
            name='Abonnement',
        ),
        migrations.DeleteModel(
            name='Balance',
        ),
        migrations.DeleteModel(
            name='Classes',
        ),
        migrations.DeleteModel(
            name='TransfertCredit',
        ),
        migrations.AddField(
            model_name='compteur',
            name='classe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='compteur.Classe'),
        ),
    ]
