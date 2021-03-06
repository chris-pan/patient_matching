# Generated by Django 3.0.4 on 2020-03-29 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.IntegerField()),
                ('patient_id', models.IntegerField()),
                ('patient_account_num', models.IntegerField()),
                ('first_name', models.CharField(max_length=50)),
                ('middle_initial', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('dob', models.CharField(max_length=50)),
                ('sex', models.CharField(max_length=50)),
                ('cur_street1', models.CharField(max_length=50)),
                ('cur_street2', models.CharField(max_length=50)),
                ('cur_city', models.CharField(max_length=50)),
                ('cur_zip', models.IntegerField()),
                ('prev_first_name', models.CharField(max_length=50)),
                ('prev_middle_initial', models.CharField(max_length=50)),
                ('prev_last_name', models.CharField(max_length=50)),
                ('prev_street_1', models.CharField(max_length=50)),
                ('prev_street_2', models.CharField(max_length=50)),
                ('prev_city', models.CharField(max_length=50)),
                ('prev_state', models.CharField(max_length=50)),
                ('prev_zip', models.IntegerField()),
            ],
        ),
    ]
