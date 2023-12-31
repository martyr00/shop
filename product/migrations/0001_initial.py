# Generated by Django 4.2.2 on 2023-06-26 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import psqlextra.indexes.unique_index


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='title')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Features',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='title')),
                ('text', models.CharField(blank=True, max_length=200, null=True, verbose_name='text')),
                ('price', models.CharField(max_length=50, verbose_name='price')),
                ('description', models.CharField(max_length=500, verbose_name='description')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created_time')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='update_time')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category')),
                ('features', models.ManyToManyField(to='product.features')),
            ],
        ),
        migrations.CreateModel(
            name='ProductRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.BooleanField()),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created_time')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [psqlextra.indexes.unique_index.UniqueIndex(fields=['user', 'product'], name='product_pro_user_id_f85649_idx')],
            },
        ),
    ]
