# Generated by Django 4.2.4 on 2023-09-06 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_category_category_disc_delete_category_discription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_disc',
            field=models.CharField(max_length=80),
        ),
    ]
