# Generated by Django 5.0.6 on 2024-07-10 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0006_order_products'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['promocode']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-name']},
        ),
    ]

