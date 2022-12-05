# Generated by Django 3.0 on 2022-11-23 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0017_auto_20221123_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default=101, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('C', 'Cameras'), ('L', 'Laptops'), ('A', 'Accessories'), ('S', 'Smartphones')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(blank=True, choices=[('S', 'sale'), ('N', 'new')], max_length=1, null=True),
        ),
    ]
