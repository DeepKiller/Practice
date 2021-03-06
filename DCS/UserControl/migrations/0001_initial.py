# Generated by Django 3.1.3 on 2020-12-02 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('Password', models.CharField(max_length=254)),
                ('IsConfimed', models.BooleanField(default=False)),
                ('Role', models.CharField(choices=[('Admin', 'Admin'), ('User', 'User')], default='User', max_length=20)),
                ('DateCreated', models.DateField()),
                ('DateUpdated', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
