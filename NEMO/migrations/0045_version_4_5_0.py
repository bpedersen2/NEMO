# Generated by Django 3.2.16 on 2023-01-25 14:49

import django.db.models.deletion
from django.db import migrations, models

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

    operations = [
        migrations.RunPython(new_version_news),
        migrations.AlterModelOptions(
            name='temporaryphysicalaccess',
            options={'ordering': ['-end_time'], 'verbose_name_plural': 'TemporaryPhysicalAccess'},
        ),
        migrations.RenameModel(
            old_name='Discipline',
            new_name='ProjectDiscipline',
        ),
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('news', 'News creation and updates - notifies all users'), ('safetyissue', 'New safety issues - notifies staff only'), ('buddyrequest', 'New buddy request - notifies all users'), ('buddyrequestmessage', 'New buddy request reply - notifies request creator and users who have replied'), ('temporaryphysicalaccessrequest', 'New access request - notifies other users on request and reviewers')], max_length=100, null=True),
        ),
        migrations.RunPython(migrate_notification_types),
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
    ]

