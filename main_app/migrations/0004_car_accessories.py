# Generated by Django 2.2 on 2019-06-13 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20190612_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='accessories',
            field=models.ManyToManyField(to='main_app.Accessory'),
        ),
    ]
