# Generated by Django 4.0.6 on 2022-07-30 18:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mailing', '0004_mail_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='mail',
            name='mail_filter',
        ),
        migrations.RemoveField(
            model_name='client',
            name='tag',
        ),
        migrations.AlterField(
            model_name='mail',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='mails', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mail',
            name='code_filter',
            field=models.ManyToManyField(to='mailing.tag'),
        ),
        migrations.AddField(
            model_name='mail',
            name='tag_filter',
            field=models.ManyToManyField(to='mailing.code'),
        ),
        migrations.AlterField(
            model_name='client',
            name='code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.code'),
        ),
        migrations.AddField(
            model_name='client',
            name='tag',
            field=models.ManyToManyField(to='mailing.tag'),
        ),
    ]