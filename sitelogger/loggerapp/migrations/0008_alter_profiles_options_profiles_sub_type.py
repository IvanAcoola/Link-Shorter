# Generated by Django 4.1 on 2022-08-07 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loggerapp', '0007_alter_passes_owner_link'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profiles',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.AddField(
            model_name='profiles',
            name='sub_type',
            field=models.CharField(choices=[('JANUARY', 'January'), ('FEBRUARY', 'February'), ('MARCH', 'March'), ('DECEMBER', 'December')], default='JANUARY', max_length=10),
        ),
    ]