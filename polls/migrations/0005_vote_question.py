# Generated by Django 4.1 on 2022-09-18 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0004_remove_choice_votes_vote"),
    ]

    operations = [
        migrations.AddField(
            model_name="vote",
            name="question",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="polls.question",
            ),
        ),
    ]
