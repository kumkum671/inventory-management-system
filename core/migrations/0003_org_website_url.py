# Generated by Django 4.2 on 2024-05-10 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_org_userprofile_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='website_url',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]