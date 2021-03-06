# Generated by Django 3.1.2 on 2020-10-10 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_cart_paymentmethod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodity',
            name='formerprice',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='commodity',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='order',
            name='commodity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.commodity'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
