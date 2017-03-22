# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-21 20:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='Username')),
                ('email', models.EmailField(max_length=255, verbose_name='Email Address')),
                ('first_name', models.CharField(max_length=45, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=45, verbose_name='Last Name')),
                ('groups', models.CharField(choices=[('BKR', 'Booker'), ('ART', 'Artist')], max_length=3, verbose_name='Access')),
                ('phone', models.CharField(max_length=11, verbose_name='Phone')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_name', models.CharField(max_length=100)),
                ('site', models.URLField(blank=True)),
                ('sound', models.URLField(blank=True)),
                ('about', models.TextField(blank=True)),
                ('artist_photo', models.ImageField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contact_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('Pend', 'Pending Event'), ('Acpt', 'Accepted Event'), ('Decl', 'Declined Event')], default='Pend', max_length=45)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('artist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookr.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookr.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(choices=[('SEA', 'Seattle'), ('SFO', 'San Francisco')], max_length=45)),
                ('state', models.CharField(choices=[('WA', 'Washington'), ('CA', 'California')], max_length=2)),
                ('zipcode', models.CharField(max_length=5)),
                ('venue_phone', models.CharField(max_length=10)),
                ('venue_photo', models.ImageField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('booker_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='venue_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookr.Venue'),
        ),
        migrations.AddField(
            model_name='comment',
            name='event_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookr.Event'),
        ),
        migrations.AddField(
            model_name='comment',
            name='message_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookr.Message'),
        ),
    ]
