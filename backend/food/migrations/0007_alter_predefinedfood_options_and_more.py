# Generated by Django 5.2.1 on 2025-05-24 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0006_alter_predefinedfood_options_sidefishes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='predefinedfood',
            options={'verbose_name': 'غذای پیش تعریف شده', 'verbose_name_plural': 'غذاهای از پیش تعریف شده'},
        ),
        migrations.AlterModelOptions(
            name='sidefishes',
            options={'verbose_name': 'ویژگی اضافه', 'verbose_name_plural': 'ویژگی های اضافه'},
        ),
        migrations.AddField(
            model_name='sidefishes',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='sidefishes',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
        migrations.AddField(
            model_name='sidefishes',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
