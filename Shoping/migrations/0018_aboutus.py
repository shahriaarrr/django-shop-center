# Generated by Django 3.2.4 on 2021-07-26 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shoping', '0017_auto_20210726_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='توضیحات')),
            ],
        ),
    ]
