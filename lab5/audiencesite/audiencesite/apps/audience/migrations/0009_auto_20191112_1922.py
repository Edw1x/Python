# Generated by Django 2.2.6 on 2019-11-12 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audience', '0008_auto_20191112_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date_end',
            field=models.DateTimeField(default='0000-00-00 00:00:00'),
        ),
    ]
