# Generated by Django 3.2 on 2022-12-31 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]