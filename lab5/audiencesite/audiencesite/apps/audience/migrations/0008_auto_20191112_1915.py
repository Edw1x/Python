# Generated by Django 2.2.6 on 2019-11-12 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audience', '0007_order_order_date_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date_end',
            field=models.DateTimeField(default='YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]'),
        ),
    ]
