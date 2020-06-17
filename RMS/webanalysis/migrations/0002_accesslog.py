# Generated by Django 3.0.7 on 2020-06-17 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webanalysis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_id', models.IntegerField(default=0)),
                ('ip', models.CharField(default='', max_length=128)),
                ('url', models.CharField(default='', max_length=1024)),
                ('status_code', models.IntegerField(default=0)),
                ('access_time', models.DateTimeField()),
            ],
        ),
    ]
