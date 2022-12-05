# Generated by Django 3.0 on 2022-11-21 10:33

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0008_auto_20221121_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryaddress',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('A', 'Accessories'), ('C', 'Cameras'), ('S', 'Smartphones'), ('L', 'Laptops')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(blank=True, choices=[('N', 'new'), ('S', 'sale')], max_length=1, null=True),
        ),
    ]
