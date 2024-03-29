# Generated by Django 2.1.7 on 2019-04-02 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_embedded'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='link',
            field=models.URLField(blank=True, max_length=250, null=True, verbose_name='Links de outras fontes'),
        ),
        migrations.AlterField(
            model_name='post',
            name='embedded',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Link para video externo'),
        ),
    ]
