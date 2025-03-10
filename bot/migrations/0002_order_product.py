# Generated by Django 3.1.1 on 2024-04-29 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, null=True, verbose_name='Назва послуги')),
                ('question', models.TextField(null=True, verbose_name='Опис')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=256, null=True, verbose_name='Час')),
                ('location', models.CharField(max_length=256, null=True, verbose_name='Локація')),
                ('contact', models.CharField(max_length=256, null=True, verbose_name='Контакти')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.userprofile')),
            ],
        ),
    ]
