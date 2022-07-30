# Generated by Django 4.0.6 on 2022-07-30 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mailing', '0003_rename_filter_mail_mail_filter'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='owner',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, related_name='snippets', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]