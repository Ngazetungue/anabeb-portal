# Generated by Django 5.1.6 on 2025-03-08 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="guard",
            name="home_language",
        ),
    ]
