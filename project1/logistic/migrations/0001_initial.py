# Generated by Django 4.0.5 on 2022-06-20 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ToDo', models.FloatField(null=True)),
                ('Done', models.FloatField(null=True)),
                ('Contrag', models.CharField(max_length=1000, null=True)),
                ('Amount_Cars', models.CharField(max_length=10, null=True)),
                ('Num_Cars', models.CharField(max_length=2000, null=True)),
                ('Time', models.DateTimeField(null=True)),
            ],
        ),
    ]
