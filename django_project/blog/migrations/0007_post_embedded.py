# Generated by Django 2.1.7 on 2019-04-01 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20190331_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='embedded',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Link externo'),
        ),
    ]
