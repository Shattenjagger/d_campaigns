# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 07:24
from __future__ import unicode_literals

from django.db import migrations, models
import recurrence.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(null=True)),
                ('recurrence', recurrence.fields.RecurrenceField()),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
