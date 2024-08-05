# Generated by Django 5.0.6 on 2024-06-18 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('selling_price', models.FloatField()),
                ('discounted_price', models.FloatField()),
                ('description', models.TextField()),
                ('composition', models.TextField(default='')),
                ('prodapp', models.TextField(default='')),
                ('category', models.CharField(choices=[('ML', 'Milk'), ('CR', 'Curd'), ('GH', 'Ghee'), ('PN', 'Paneer'), ('CH', 'Cheese'), ('IC', 'Ice Cream'), ('FL', 'Flavored Milk'), ('BV', 'Beverage')], max_length=2)),
                ('product_image', models.ImageField(upload_to='product')),
            ],
        ),
    ]
