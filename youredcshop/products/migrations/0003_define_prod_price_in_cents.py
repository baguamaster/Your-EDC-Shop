from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210515_1251'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='price_in_cents',
        ),
    ]