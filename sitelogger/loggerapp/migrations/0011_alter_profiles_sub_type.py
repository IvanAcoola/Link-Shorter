# Generated by Django 4.1 on 2022-08-07 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loggerapp', '0010_alter_profiles_sub_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='sub_type',
            field=models.CharField(choices=[('pro', 'pro'), ('vip', 'vip'), ('max', 'max')], default='pro', max_length=10),
        ),
    ]