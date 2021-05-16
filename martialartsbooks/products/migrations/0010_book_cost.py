# Generated by Django 3.1.7 on 2021-04-03 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_book_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cost',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
