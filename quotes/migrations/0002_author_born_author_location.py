# Generated by Django 4.1.7 on 2023-02-20 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='born',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='location',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
