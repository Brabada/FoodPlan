# Generated by Django 4.2.5 on 2023-09-22 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='allergies',
            field=models.ManyToManyField(blank=True, related_name='allergy_subscriptions', to='baseapp.allergy', verbose_name='Аллергии'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='meal_types',
            field=models.ManyToManyField(blank=True, related_name='subscriptions', to='baseapp.mealtype', verbose_name='Типы приемов пищи'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='today_dishes',
            field=models.ManyToManyField(blank=True, related_name='dish_subscriptions', to='baseapp.dish', verbose_name='Сегодняшние блюда подписки'),
        ),
    ]
