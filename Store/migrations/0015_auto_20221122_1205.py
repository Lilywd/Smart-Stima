# Generated by Django 3.0 on 2022-11-22 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0014_auto_20221121_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='amount',
            field=models.FloatField(default=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('L', 'Laptops'), ('A', 'Accessories'), ('C', 'Cameras'), ('S', 'Smartphones')], max_length=2),
        ),
    ]
