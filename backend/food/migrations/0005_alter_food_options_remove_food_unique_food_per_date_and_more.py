# Generated by Django 5.2.1 on 2025-05-24 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_predefinedfood_alter_fooddate_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='food',
            options={},
        ),
        migrations.RemoveConstraint(
            model_name='food',
            name='unique_food_per_date',
        ),
        migrations.AlterField(
            model_name='predefinedfood',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='نام غذا'),
        ),
    ]
