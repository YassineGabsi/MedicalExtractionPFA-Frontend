# Generated by Django 3.1.4 on 2021-04-18 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icd10', '0003_auto_20210418_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchproject',
            name='end_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='researchproject',
            name='project_file_url',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='researchproject',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='researchproject',
            name='status',
            field=models.CharField(choices=[('S', 'Started'), ('C', 'Completed'), ('E', 'Error')], default='S', max_length=30),
        ),
    ]
