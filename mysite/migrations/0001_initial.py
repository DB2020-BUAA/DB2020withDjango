# Generated by Django 3.1.4 on 2020-12-22 18:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mysite.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('info', models.TextField()),
                ('name', models.TextField(default='default')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('info', models.TextField(max_length=100, null=True)),
                ('create_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('info', models.TextField()),
                ('name', models.TextField(default='default')),
                ('imgs', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('info', models.TextField(max_length=100, null=True)),
                ('avatar', models.IntegerField(choices=[(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')], default=1)),
                ('django_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserToGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('linked_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.group')),
                ('linked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='UpdToExp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('linked_exp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.experiment')),
                ('linked_upd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.update')),
            ],
        ),
        migrations.CreateModel(
            name='UpdateData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('info', models.TextField()),
                ('name', models.TextField(default='default')),
                ('data', models.FileField(upload_to=mysite.models.user_data_path)),
                ('file_type', models.CharField(max_length=6, null=True)),
                ('create_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data_creator', to='mysite.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='update',
            name='create_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='update_creator', to='mysite.userprofile'),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('info', models.TextField()),
                ('status', models.IntegerField(default=0)),
                ('answer_date', models.DateTimeField(auto_now=True)),
                ('answer_info', models.TextField()),
                ('create_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issue_creator', to='mysite.userprofile')),
                ('target_update', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.update')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='group_master', to='mysite.userprofile'),
        ),
        migrations.CreateModel(
            name='ExpToGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('linked_exp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.experiment')),
                ('linked_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.group')),
            ],
        ),
        migrations.AddField(
            model_name='experiment',
            name='create_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exp_creator', to='mysite.userprofile'),
        ),
        migrations.CreateModel(
            name='DataToUpd',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('linked_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.updatedata')),
                ('linked_upd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.update')),
            ],
        ),
        migrations.CreateModel(
            name='Compare',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('info', models.TextField()),
                ('create_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='compare_creator', to='mysite.userprofile')),
                ('upd1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compare_update1', to='mysite.update')),
                ('upd2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compare_update2', to='mysite.update')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('info', models.TextField()),
                ('create_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_creator', to='mysite.userprofile')),
                ('target_update', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.update')),
            ],
        ),
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('info', models.TextField()),
                ('status', models.IntegerField(default=0)),
                ('reply_time', models.DateTimeField(auto_now=True)),
                ('reply', models.BooleanField(default=False)),
                ('create_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='apply_creator', to='mysite.userprofile')),
                ('target_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apply_target', to='mysite.group')),
            ],
        ),
    ]
