# Generated by Django 3.0.8 on 2020-07-25 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyLibrary', '0003_auto_20200725_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_id',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
