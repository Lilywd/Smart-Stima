# Generated by Django 3.0 on 2022-12-06 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0024_auto_20221206_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_method',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('S', 'Smartphones'), ('A', 'Accessories'), ('C', 'Cameras'), ('L', 'Laptops')], max_length=2),
        ),
    ]
