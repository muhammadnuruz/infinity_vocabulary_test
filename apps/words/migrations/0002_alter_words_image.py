# Generated by Django 5.0.1 on 2024-08-02 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='words',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]