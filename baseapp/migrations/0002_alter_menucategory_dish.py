# Generated by Django 4.2.5 on 2023-09-22 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menucategory',
            name='dish',
            field=models.ManyToManyField(related_name='menu_categories', to='baseapp.dish', verbose_name='Блюда'),
        ),
    ]
