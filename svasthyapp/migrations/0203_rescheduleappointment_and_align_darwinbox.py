import django.db.models.deletion
from django.db import migrations, models
import svasthyapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('svasthyapp', '0202_darwinboxcandidateappointment'),
    ]

    operations = [
        migrations.CreateModel(
            name='RescheduleAppointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rescheduled_by', models.CharField(blank=True, max_length=200, null=True, verbose_name='rescheduled_by')),
                ('old_appointment_date', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='old_appointment_date')),
                ('new_appointment_date', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='new_appointment_date')),
                ('old_home_sample_date', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='old_home_sample_date')),
                ('new_home_sample_date', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='new_home_sample_date')),
                ('reason', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='reason')),
                ('remark', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='remark')),
                ('status', models.CharField(default='Rescheduled', max_length=200, null=True, verbose_name='status')),
                ('created_at', models.CharField(max_length=200, null=True, verbose_name='created_at')),
                ('appointment', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='svasthyapp.appointmentdetail', verbose_name='appointment')),
            ],
        ),
        migrations.CreateModel(
            name='RescheduleDarwinboxCandidateAppointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rescheduled_by', models.CharField(blank=True, max_length=200, null=True, verbose_name='rescheduled_by')),
                ('old_appointment_date', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='old_appointment_date')),
                ('new_appointment_date', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='new_appointment_date')),
                ('old_home_sample_date', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='old_home_sample_date')),
                ('new_home_sample_date', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='new_home_sample_date')),
                ('reason', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='reason')),
                ('remark', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='remark')),
                ('status', models.CharField(default='Rescheduled', max_length=200, null=True, verbose_name='status')),
                ('created_at', models.CharField(max_length=200, null=True, verbose_name='created_at')),
                ('appointment', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='svasthyapp.darwinboxcandidateappointment', verbose_name='appointment')),
                ('hoh_employee', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='svasthyapp.hohemployee', verbose_name='HOH Employee')),
            ],
        ),
        migrations.AddField(
            model_name='darwinboxcandidateappointment',
            name='appointment_date_1',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='appointment_date_1'),
        ),
        migrations.AddField(
            model_name='darwinboxcandidateappointment',
            name='appointment_date_2',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='appointment_date_2'),
        ),
        migrations.AddField(
            model_name='darwinboxcandidateappointment',
            name='home_sample_date_1',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='home_sample_date_1'),
        ),
        migrations.AddField(
            model_name='darwinboxcandidateappointment',
            name='home_sample_date_2',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='home_sample_date_2'),
        ),
        migrations.AddField(
            model_name='darwinboxcandidateappointment',
            name='confirm_appointment_date',
            field=models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='confirm_appointment_date'),
        ),
        migrations.AddField(
            model_name='darwinboxcandidateappointment',
            name='confirm_home_sample_date',
            field=models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='confirm_home_sample_date'),
        ),
        migrations.AddField(
            model_name='darwinboxcandidateappointment',
            name='date_of_appointment',
            field=models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='date_of_appointment'),
        ),
        migrations.AddField(
            model_name='darwinboxcandidateappointment',
            name='reason',
            field=models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='reason'),
        ),
        migrations.AddField(
            model_name='darwinboxcandidateappointment',
            name='remark',
            field=models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='remark'),
        ),
        migrations.AddField(
            model_name='darwinboxcandidateappointment',
            name='report_date',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='report_date'),
        ),
        migrations.AddField(
            model_name='darwinboxcandidateappointment',
            name='report',
            field=models.FileField(blank=True, null=True, upload_to='image/Report', validators=[svasthyapp.validators.validate_file_extension_image_and_pdf], verbose_name='report'),
        ),
        migrations.AddField(
            model_name='darwinboxcandidateappointment',
            name='status',
            field=models.CharField(max_length=200, null=True, verbose_name='status'),
        ),
        migrations.AddField(
            model_name='darwinboxcandidateappointment',
            name='type_of_visit',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='svasthyapp.typeofvisit', verbose_name='type_of_visit'),
        ),
        migrations.AlterField(
            model_name='darwinboxcandidateappointment',
            name='center',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='svasthyapp.centerdetail', verbose_name='Center'),
        ),
        migrations.AlterField(
            model_name='darwinboxcandidateappointment',
            name='created_at',
            field=models.CharField(max_length=200, null=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='darwinboxcandidateappointment',
            name='hoh_employee',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='svasthyapp.hohemployee', verbose_name='HOH Employee'),
        ),
        migrations.AlterField(
            model_name='darwinboxcandidateappointment',
            name='package',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='svasthyapp.packagedetail', verbose_name='package'),
        ),
        migrations.AlterField(
            model_name='darwinboxcandidateappointment',
            name='vendor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='svasthyapp.vendordetail', verbose_name='vendor'),
        ),
    ]
