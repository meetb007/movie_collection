# Generated by Django 4.1.7 on 2023-03-24 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='title',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, unique=True),
        ),
    ]