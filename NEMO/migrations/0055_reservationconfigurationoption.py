# Generated by Django 3.2.22 on 2023-11-28 18:58
import re

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("NEMO", "0054_documents_update_max_length"),
    ]

    def migrate_configuration_option_forward(apps, schema_editor):
        ConfigurationHistory = apps.get_model("NEMO", "ConfigurationHistory")
        ConfigurationOption = apps.get_model("NEMO", "ConfigurationOption")
        Reservation = apps.get_model("NEMO", "Reservation")
        for reservation in Reservation.objects.exclude(additional_information="").exclude(
            additional_information__isnull=True
        ):
            configs = extract_patterns_in_additional_information(reservation.additional_information)
            for config in configs:
                name, value = config[0].strip(), config[1].strip()
                ConfigurationOption.objects.create(name=name, reservation=reservation, current_setting=value)
        for config_history in ConfigurationHistory.objects.all():
            conf = config_history.configuration
            config_history.item_name = (
                f"{conf.configurable_item_name} #{config_history.slot + 1}"
                if conf.configurable_item_name
                else conf.name
            )
            config_history.save()

    def migrate_configuration_option_reverse(apps, schema_editor):
        pass

    operations = [
        migrations.AlterField(
            model_name="area",
            name="area_calendar_color",
            field=models.CharField(
                default="#88B7CD",
                help_text="Color for tool reservations in calendar overviews",
                max_length=9,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"),
                        "Enter a valid hex color, eg. #000000",
                        "invalid",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="tool",
            name="_tool_calendar_color",
            field=models.CharField(
                db_column="tool_calendar_color",
                default="#33ad33",
                help_text="Color for tool reservations in calendar overviews",
                max_length=9,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"),
                        "Enter a valid hex color, eg. #000000",
                        "invalid",
                    )
                ],
            ),
        ),
        migrations.AddField(
            model_name="configurationhistory",
            name="item_name",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="configuration",
            name="calendar_colors",
            field=models.TextField(
                blank=True,
                help_text="Comma separated list of html colors for each available setting. E.g. #ffffff, #eeeeee",
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})(?:,\\s*#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3}))*$"),
                        code="invalid",
                        message="Enter a valid hex color list, eg. #000000,#111111",
                    )
                ],
            ),
        ),
        migrations.CreateModel(
            name="ConfigurationOption",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                (
                    "current_setting",
                    models.CharField(
                        blank=True,
                        help_text="The current value for this configuration option",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "available_settings",
                    models.TextField(
                        blank=True,
                        help_text="The available choices to select for this configuration option. Multiple values are separated by commas.",
                        null=True,
                    ),
                ),
                (
                    "calendar_colors",
                    models.TextField(
                        blank=True,
                        help_text="Comma separated list of html colors for each available setting. E.g. #ffffff, #eeeeee",
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile(
                                    "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})(?:,\\s*#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3}))*$"
                                ),
                                code="invalid",
                                message="Enter a valid hex color list, eg. #000000,#111111",
                            )
                        ],
                    ),
                ),
                (
                    "absence_string",
                    models.CharField(
                        blank=True,
                        help_text="The text that appears to indicate absence of a choice.",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "configuration",
                    models.ForeignKey(
                        blank=True,
                        help_text="The configuration this option applies to",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="NEMO.configuration",
                    ),
                ),
                (
                    "reservation",
                    models.ForeignKey(
                        help_text="The reservation this option is set on",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="configurationoption_set",
                        to="NEMO.reservation",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RunPython(migrate_configuration_option_forward, migrate_configuration_option_reverse),
    ]


def extract_patterns_in_additional_information(sentence):
    # Define the pattern using regular expressions
    # pattern = r"(.*?)\s+(?:#\d+\s+)?needs\s+to\s+be\s+set\s+to\s+(.*?)\."
    pattern = r"(.*?)\s+needs\s+to\s+be\s+set\s+to\s+(.*?)\."

    # Find all matches in the sentence
    matches = re.findall(pattern, sentence)

    return matches
