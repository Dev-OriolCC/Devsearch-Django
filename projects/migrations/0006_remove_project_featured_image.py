# Generated by Django 3.2.6 on 2021-08-26 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_project_featured_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='featured_image',
        ),
    ]