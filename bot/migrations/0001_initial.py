# Generated by Django 3.1.1 on 2024-04-29 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.BigIntegerField(null=True)),
                ('username', models.CharField(max_length=256, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'userprofile',
            },
        ),
    ]
