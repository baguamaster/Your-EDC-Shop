from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20210507_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
    ]