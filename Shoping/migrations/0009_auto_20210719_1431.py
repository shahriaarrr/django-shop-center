# Generated by Django 3.2.5 on 2021-07-19 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shoping', '0008_product_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'محصولات', 'verbose_name_plural': 'محصولات'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=False, verbose_name='فعال / غیرفعال'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image/', verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(verbose_name='قیمت'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=120, verbose_name='عنوان'),
        ),
    ]
