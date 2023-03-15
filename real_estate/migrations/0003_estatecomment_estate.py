# Generated by Django 4.1.4 on 2022-12-25 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0002_estatecomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='estatecomment',
            name='estate',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='real_estate.realestate'),
            preserve_default=False,
        ),
    ]