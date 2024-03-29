# Generated by Django 5.0.2 on 2024-03-01 08:44

import django.db.models.deletion
import django.db.models.fields
import multiselectfield.db.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('address', models.CharField(max_length=500)),
                ('College_picture', models.ImageField(blank=True, upload_to='thumbpath')),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sem_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('desc', models.CharField(max_length=500)),
                ('pdf', models.FileField(upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])),
                ('rated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings_given', to=settings.AUTH_USER_MODEL)),
                ('rated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings_received', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', multiselectfield.db.fields.MultiSelectField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=9)),
                ('profile_picture', models.ImageField(blank=True, upload_to='media')),
                ('usertype', multiselectfield.db.fields.MultiSelectField(choices=[('student', 'Student'), ('professor', 'Professor')], default='student', max_length=9)),
                ('average_rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=3)),
                ('College', models.ForeignKey(null=True, on_delete=django.db.models.fields.NullBooleanField, to='webpages.college')),
                ('Semester', models.ForeignKey(null=True, on_delete=django.db.models.fields.NullBooleanField, to='webpages.semester')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
