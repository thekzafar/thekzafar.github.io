# Generated by Django 3.0.8 on 2020-07-25 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyLibrary', '0006_auto_20200725_2102'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
    ]
