# Generated by Django 4.1.7 on 2023-03-13 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tr_registration_date', models.DateField()),
                ('tr_last_year_performance', models.CharField(max_length=100)),
                ('tr_player', models.ManyToManyField(to='application.tennisplayer')),
                ('tr_tournament', models.ManyToManyField(to='application.tournament')),
            ],
        ),
    ]
