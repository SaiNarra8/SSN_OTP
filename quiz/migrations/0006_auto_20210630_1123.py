# Generated by Django 3.2.4 on 2021-06-30 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20201209_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='mp3file',
            field=models.FileField(default=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.CharField(max_length=200),
        ),
    ]