# Generated by Django 4.2.1 on 2023-09-21 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblio', '0006_livre_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livre',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='static/bookcovers'),
        ),
    ]
