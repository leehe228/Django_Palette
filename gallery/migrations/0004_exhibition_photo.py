# Generated by Django 2.0.13 on 2020-11-09 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20201107_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibition',
            name='photo',
            field=models.ImageField(null=True, upload_to=models.IntegerField(db_index=True, default=-1, primary_key=True, serialize=False, unique=True)),
        ),
    ]
