# Generated by Django 3.0.8 on 2020-10-15 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inputs', '0016_lookupset_assessment_txt_lu'),
    ]

    operations = [
        migrations.AddField(
            model_name='lookupset',
            name='goals_lu',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='lookupset',
            name='goals_txt_lu',
            field=models.CharField(default='', max_length=1000),
        ),
    ]