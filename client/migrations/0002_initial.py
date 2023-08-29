# Generated by Django 4.2.4 on 2023-08-16 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='mailing_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mailing.mail'),
        ),
    ]