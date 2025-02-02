# Generated by Django 4.2.6 on 2023-10-28 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('election_pollserver', '0003_remove_election_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voter',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='voter',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='voter',
            name='voted_in',
        ),
        migrations.AddField(
            model_name='voter',
            name='election',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='election_pollserver.election'),
        ),
        migrations.AddField(
            model_name='voter',
            name='voted_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='election_pollserver.party'),
        ),
    ]
