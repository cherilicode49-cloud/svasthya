
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            'svasthyapp',
            '0210_darwinboxcandidateappointment_appointment_time_slot_1_and_more',
        ),
    ]

    operations = [
        # These columns already exist in SQL Server.
        # Add them to Django's migration state without recreating them.
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AddField(
                    model_name='darwinboxcandidateappointment',
                    name='time_slot',
                    field=models.CharField(
                        blank=True,
                        default=None,
                        max_length=200,
                        null=True,
                        verbose_name='time_slot',
                    ),
                ),
            ],
        ),

        # These six columns are missing from svasthyapp_hohemployee.
        migrations.AddField(
            model_name='hohemployee',
            name='member_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hohemployee',
            name='recruiter_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='hohemployee',
            name='recruiter_mobile',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='hohemployee',
            name='recruiter_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hohemployee',
            name='remark',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hohemployee',
            name='status',
            field=models.CharField(
                blank=True,
                choices=[
                    ('Contacted', 'Contacted'),
                    ('Person Not Approachable', 'Person Not Approachable'),
                    ('Pending from Employee', 'Pending from Employee'),
                ],
                max_length=50,
                null=True,
            ),
        ),

        # These columns also already exist in SQL Server.
        # Record them in Django's state without adding duplicate columns.
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AddField(
                    model_name='rescheduledarwinboxcandidateappointment',
                    name='new_time_slot',
                    field=models.CharField(
                        blank=True,
                        default=None,
                        max_length=200,
                        null=True,
                        verbose_name='new_time_slot',
                    ),
                ),
                migrations.AddField(
                    model_name='rescheduledarwinboxcandidateappointment',
                    name='old_time_slot',
                    field=models.CharField(
                        blank=True,
                        default=None,
                        max_length=200,
                        null=True,
                        verbose_name='old_time_slot',
                    ),
                ),
                migrations.AddField(
                    model_name='rescheduledarwinboxcandidateappointment',
                    name='time_slot',
                    field=models.CharField(
                        blank=True,
                        default=None,
                        max_length=200,
                        null=True,
                        verbose_name='time_slot',
                    ),
                ),
            ],
        ),
    ]
