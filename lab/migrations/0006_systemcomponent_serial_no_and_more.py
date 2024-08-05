# Generated by Django 4.2 on 2024-07-09 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0005_alter_system_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemcomponent',
            name='serial_no',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='systemcomponent',
            name='system',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lab.system'),
        ),
    ]