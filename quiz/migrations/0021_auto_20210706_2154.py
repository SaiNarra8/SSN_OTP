# Generated by Django 3.2.4 on 2021-07-06 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0020_auto_20210704_1123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='email',
        ),
        migrations.RemoveField(
            model_name='question',
            name='is_email',
        ),
        migrations.RemoveField(
            model_name='question',
            name='is_paragraph',
        ),
        migrations.RemoveField(
            model_name='question',
            name='passage',
        ),
    ]