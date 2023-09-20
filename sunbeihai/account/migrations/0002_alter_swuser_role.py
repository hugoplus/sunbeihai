# Generated by Django 4.2.4 on 2023-08-25 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swuser',
            name='role',
            field=models.CharField(choices=[('administrator', 'Administrator'), ('author', 'Author'), ('editor', 'Editor'), ('reader', 'Reader'), ('partner', 'Partner')], default='author', max_length=100),
        ),
    ]