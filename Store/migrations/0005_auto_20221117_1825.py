# Generated by Django 3.0 on 2022-11-17 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0004_auto_20221117_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('S', 'Smartphones'), ('L', 'Laptops'), ('C', 'Cameras'), ('A', 'Accessories')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(blank=True, choices=[('S', 'sale'), ('N', 'new')], max_length=1, null=True),
        ),
    ]