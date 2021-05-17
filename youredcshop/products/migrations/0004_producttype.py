from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_rename_price_product_price_in_cents'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]