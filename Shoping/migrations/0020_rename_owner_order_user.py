# Generated by Django 3.2.5 on 2021-07-27 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shoping', '0019_auto_20210727_1042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='owner',
            new_name='user',
        ),
    ]