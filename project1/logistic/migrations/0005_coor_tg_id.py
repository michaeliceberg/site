# Generated by Django 4.0.5 on 2022-06-26 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistic', '0004_coor'),
    ]

    operations = [
        migrations.AddField(
            model_name='coor',
            name='tg_id',
            field=models.IntegerField(null=True),
        ),
    ]
