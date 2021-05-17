
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20210515_1256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price_in_cents',
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(
                decimal_places=2, default=None, max_digits=19),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
