# Generated by Django 3.2 on 2021-07-21 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jewellery', '0003_auto_20210709_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='specail_prod',
            field=models.BooleanField(default=False),
        ),
    ]
