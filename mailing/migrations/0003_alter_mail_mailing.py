# Generated by Django 4.2.4 on 2023-08-16 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='mailing',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing'),
        ),
    ]