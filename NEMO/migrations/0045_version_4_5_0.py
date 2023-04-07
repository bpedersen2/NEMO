# Generated by Django 3.2.16 on 2023-01-25 14:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.db.models import F

from NEMO.migrations_utils import create_news_for_version


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('NEMO', '0044_version_4_4_0'),
    ]

    def new_version_news(apps, schema_editor):
        create_news_for_version(apps, "4.5.0", "")

    def migrate_notification_types(apps, schema_editor):
        Notification = apps.get_model('NEMO', 'Notification')
        for notification in Notification.objects.all():
            notification.notification_type = notification.content_type.model
            notification.save(update_fields=['notification_type'])

    def migrate_request_messages(apps, schema_editor):
        RequestMessage = apps.get_model('NEMO', 'RequestMessage')
        for request_message in RequestMessage.objects.all():
            request_type = apps.get_model("contenttypes", "ContentType").objects.get_for_model(request_message.buddy_request)
            request_message.content_type = request_type
            request_message.object_id = request_message.buddy_request.id
            request_message.save(update_fields=["content_type", "object_id"])

    def set_remote_work_flag(apps, schema_editor):
        UsageEvent = apps.get_model("NEMO", "UsageEvent")
        # go through all previous tool usage and set them to be remote work if operator is different from user
        for tool_usage in UsageEvent.objects.exclude(user=F("operator")):
            if tool_usage.user != tool_usage.operator:
                tool_usage.remote_work = True
                tool_usage.save(update_fields=["remote_work"])

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('news', 'News creation and updates - notifies all users'), ('safetyissue', 'New safety issues - notifies staff only'), ('buddyrequest', 'New buddy request - notifies all users'), ('buddyrequestmessage', 'New buddy request reply - notifies request creator and users who have replied'), ('temporaryphysicalaccessrequest', 'New access request - notifies other users on request and reviewers')], max_length=100, null=True),
        ),
        migrations.RunPython(migrate_notification_types),
        migrations.RunPython(new_version_news),
        migrations.AlterModelOptions(
            name='temporaryphysicalaccess',
            options={'ordering': ['-end_time'], 'verbose_name_plural': 'TemporaryPhysicalAccess'},
        ),
        migrations.RenameModel(
            old_name='Discipline',
            new_name='ProjectDiscipline',
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('news', 'News creation and updates - notifies all users'), ('safetyissue', 'New safety issues - notifies staff only'), ('buddyrequest', 'New buddy request - notifies all users'), ('buddyrequestmessage', 'New buddy request reply - notifies request creator and users who have replied'), ('temporaryphysicalaccessrequest', 'New access request - notifies other users on request and reviewers')], max_length=100),
        ),
        migrations.RenameModel(
            old_name='BuddyRequestMessage',
            new_name='RequestMessage',
        ),
        migrations.AddField(
            model_name='requestmessage',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype',
                                    null=True),
        ),
        migrations.AddField(
            model_name='requestmessage',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.RunPython(migrate_request_messages),
        migrations.AlterField(
            model_name='requestmessage',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='requestmessage',
            name='object_id',
            field=models.PositiveIntegerField(),
        ),
        migrations.RemoveField(
            model_name='requestmessage',
            name='buddy_request',
        ),
        migrations.RemoveField(
            model_name='userpreferences',
            name='display_new_buddy_request_reply_notification',
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='email_new_adjustment_request_reply',
            field=models.BooleanField(default=True, help_text='Whether or not to email the user of replies on adjustment request he commented on', verbose_name='email_new_adjustment_request_reply'),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='email_send_adjustment_request_updates',
            field=models.PositiveIntegerField(choices=[(1, 'Both emails'), (2, 'Main email only')], default=1, help_text='Adjustment request updates'),
        ),
        migrations.AlterField(
            model_name='emaillog',
            name='category',
            field=models.IntegerField(choices=[(0, 'General'), (1, 'System'), (2, 'Direct Contact'), (3, 'Broadcast Email'), (4, 'Timed Services'), (5, 'Feedback'), (6, 'Abuse'), (7, 'Safety'), (8, 'Tasks'), (9, 'Access Requests'), (10, 'Sensors'), (11, 'Adjustment Requests')], default=0),
        ),
        migrations.AlterField(
            model_name='landingpagechoice',
            name='notifications',
            field=models.CharField(blank=True, choices=[('news', 'News creation and updates - notifies all users'), ('safetyissue', 'New safety issues - notifies staff only'), ('buddyrequest', 'New buddy request - notifies all users'), ('buddyrequestmessage', 'New buddy request reply - notifies request creator and users who have replied'), ('adjustmentrequest', 'New adjustment request - notifies facility managers only'), ('adjustmentrequestmessage', 'New adjustment request reply - notifies request creator and users who have replied'), ('temporaryphysicalaccessrequest', 'New access request - notifies other users on request and reviewers')], help_text="Displays a the number of new notifications for the user. For example, if the user has two unread news notifications then the number '2' would appear for the news icon on the landing page.", max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('news', 'News creation and updates - notifies all users'), ('safetyissue', 'New safety issues - notifies staff only'), ('buddyrequest', 'New buddy request - notifies all users'), ('buddyrequestmessage', 'New buddy request reply - notifies request creator and users who have replied'), ('adjustmentrequest', 'New adjustment request - notifies facility managers only'), ('adjustmentrequestmessage', 'New adjustment request reply - notifies request creator and users who have replied'), ('temporaryphysicalaccessrequest', 'New access request - notifies other users on request and reviewers')], max_length=100),
        ),
        migrations.CreateModel(
            name='AdjustmentRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True, help_text='The date and time when the request was created.')),
                ('last_updated', models.DateTimeField(auto_now=True, help_text='The last time this request was modified.')),
                ('item_id', models.PositiveIntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, help_text='The description of the request.', null=True)),
                ('manager_note', models.TextField(blank=True, help_text="A manager's note to send to the user when a request is denied or to the user office when it is approved.", null=True)),
                ('new_start', models.DateTimeField(blank=True, null=True)),
                ('new_end', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Approved'), (2, 'Denied')], default=0)),
                ('deleted', models.BooleanField(default=False, help_text="Indicates the request has been deleted and won't be shown anymore.")),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adjustment_requests_created', to=settings.AUTH_USER_MODEL)),
                ('item_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('last_updated_by', models.ForeignKey(blank=True, help_text='The last user who modified this request.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='adjustment_requests_updated', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adjustment_requests_reviewed', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-creation_time'],
            },
        ),
        migrations.AddField(
            model_name='staffavailability',
            name='visible',
            field=models.BooleanField(default=True, help_text='Specifies whether this staff member should be displayed on the staff status page.'),
        ),
        migrations.AlterModelOptions(
            name='accounttype',
            options={'ordering': ['display_order', 'name']},
        ),
        migrations.AlterModelOptions(
            name='projectdiscipline',
            options={'ordering': ['display_order', 'name']},
        ),
        migrations.AlterModelOptions(
            name='usertype',
            options={'ordering': ['display_order', 'name']},
        ),
        migrations.AddField(
            model_name='accounttype',
            name='display_order',
            field=models.IntegerField(default=0, help_text='The display order is used to sort these items. The lowest value category is displayed first.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectdiscipline',
            name='display_order',
            field=models.IntegerField(default=0, help_text='The display order is used to sort these items. The lowest value category is displayed first.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usertype',
            name='display_order',
            field=models.IntegerField(default=0, help_text='The display order is used to sort these items. The lowest value category is displayed first.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accounttype',
            name='name',
            field=models.CharField(help_text='The unique name for this item', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='usertype',
            name='name',
            field=models.CharField(help_text='The unique name for this item', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='interlock',
            name='unit_id',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Multiplier/Unit id'),
        ),
        migrations.AlterField(
            model_name='safetyissue',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='areaaccessrecord',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='consumablewithdraw',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reservation',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trainingsession',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usageevent',
            name='remote_work',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(set_remote_work_flag),
    ]

