from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_auto_20210507_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='purchase',
            name='qty',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='purchase',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]