# Generated by Django 4.1 on 2022-09-18 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_vote_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='question',
        ),
    ]