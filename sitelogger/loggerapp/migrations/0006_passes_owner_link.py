# Generated by Django 4.1 on 2022-08-06 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loggerapp', '0005_links_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='passes',
            name='owner_link',
            field=models.CharField(default='none', max_length=50),
        ),
    ]