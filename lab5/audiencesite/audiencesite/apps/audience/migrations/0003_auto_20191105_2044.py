# Generated by Django 2.2.6 on 2019-11-05 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audience', '0002_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_complete',
        ),
        migrations.AddField(
            model_name='order',
            name='order_address',
            field=models.CharField(max_length=200, null=True, verbose_name='Your address'),
        ),
    ]
