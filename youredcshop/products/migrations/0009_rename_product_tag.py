from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20210515_1261'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='tags',
            new_name='tag',
        ),
    ]
