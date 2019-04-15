# Generated by Django 2.1.7 on 2019-03-31 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20190331_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='autor',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Autor'),
        ),
        migrations.AddField(
            model_name='document',
            name='capa',
            field=models.ImageField(blank=True, null=True, upload_to='arquivos'),
        ),
        migrations.AddField(
            model_name='document',
            name='titulo',
            field=models.CharField(blank=True, max_length=255, verbose_name='Título'),
        ),
        migrations.AlterField(
            model_name='document',
            name='description',
            field=models.CharField(blank=True, max_length=255, verbose_name='Título'),
        ),
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to='documents/', verbose_name='Arquivo'),
        ),
    ]
