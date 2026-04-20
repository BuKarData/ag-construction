from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oferty', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='oferta',
            name='ogrodek_metraz',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Ogródek (m²)'),
        ),
    ]
