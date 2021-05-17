from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_producttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='products.producttype'),
            preserve_default=False,
        ),
    ]