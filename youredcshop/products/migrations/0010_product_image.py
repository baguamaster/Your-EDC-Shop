from django.db import migrations
import pyuploadcare.dj.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_rename_product_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=pyuploadcare.dj.models.ImageField(blank=True),
        ),
    ]