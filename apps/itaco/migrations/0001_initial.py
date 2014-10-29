# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import itaco.models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BillingPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
            options={
                'ordering': ['start'],
                'verbose_name_plural': 'Billing Periods',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BoardPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('credit', models.IntegerField(help_text=b'Amount deducted from tuition for holding this position. <b>Only change this when school policy chances.</b> If multiple people hold this position, this credit will automatically be split between them.')),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name_plural': 'Board Positions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('type', models.CharField(help_text=b'<strong>Please enter amounts in the following units:</strong><br />Hourly regular day care, drop-in hourly daycare, pre-arranged vacation daycare: HOURS (e.g. 2.5)<br />Meal Expense: DOLLARS (K: Pizza=3,Bread=1; 1-5: Pizza=5,Bread=2)<br />Event daycare flat-fee: Select the number of children from the dropdown, and enter &quot;1&quot; for the amount, regardless the number of hours.<br />Daycare late pickup: Enter number of MINUTES after 6 p.m. that child was picked up (e.g. 37).<br />Missed housecleaning: Always enter &quot;1&quot; for the amount.<br />Missed maintenance: Enter number of HOURS (e.g. 1.5 or 3)<br />Missed fundraising: Always enter &quot;1&quot; for the amount.<br />Missed fieldtrip: Always enter &quot;1&quot; for the amount.<br />Missed meeting: Always enter &quot;1&quot; for the amount.<br />Misc adjustments: DOLLARS (e.g. 48.25)', max_length=8, choices=[(b'hrdc', b'Hourly Regular Daycare'), (b'meal', b'Meal Expense'), (b'pavdc', b'Vacation Daycare'), (b'edc1', b'Event Daycare Flat Fee - 1 Child'), (b'edc2', b'Event Daycare Flat Fee - 2 Child'), (b'edc3', b'Event Daycare Flat Fee - 3 Child'), (b'dclpu', b'Daycare Late Pickup'), (b'mshc', b'Missed Housecleaning'), (b'mmh', b'Missed Maintenance'), (b'mfrsg', b'Missed Fundraising'), (b'mftr', b'Missed Fieldtrip'), (b'mmtg', b'Missed Meeting'), (b'adj', b'Misc Adjustments')])),
                ('amount', models.FloatField()),
                ('units', models.CharField(blank=True, max_length=8, choices=[(b'units', b'Units'), (b'hours', b'Hours'), (b'dollars', b'Dollars')])),
                ('charged_amount', models.FloatField(help_text=b'DO NOT ENTER AN AMOUNT HERE. <br />After pressing save, this field will auto-calculate the dollar equivalent of entered hours, based on family financial aid factor and current hourly rates. <br /> This amount can be adjusted after saving, if necessary.', null=True, blank=True)),
                ('note', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Charges',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommitteeJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('reports_to', models.ForeignKey(to='itaco.BoardPosition')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name_plural': 'Committee Jobs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=8, choices=[(b'partpar', b'Participating Parent'), (b'aidsub', b'Aid Substitute'), (b'teachsub', b'Teacher Substitute'), (b'incorbil', b'Incorrect Billing'), (b'board', b'Board'), (b'housekp', b'Extra Housekeeping')])),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.FloatField(help_text=b'<strong>Please use the following units when entering credits. iTaco will convert to dollars automatically:</strong><br />         Board: DOLLARS<br />       Participating parent: HOURS <br /> Extra housekeeping: Hours (Note this is NOT the same as regular obligation housekeeping)<br />        Aid substitute: HOURS<br />   Teacher substitute: Hours<br />')),
                ('charged_amount', models.FloatField(help_text=b'DO NOT ENTER AN AMOUNT HERE. <br />After pressing save, this field will auto-calculate the dollar equivalent of entered hours, based on current hourly rates. <br /> This amount can be adjusted after saving, if necessary.<br /><br />If you need to change the TYPE of charge, delete this one and create a new one.', null=True, blank=True)),
                ('note', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('famname', models.CharField(max_length=128, verbose_name=b'Family Name')),
                ('notes', models.TextField(blank=True)),
                ('fa_factor', models.FloatField(default=1, verbose_name=b'Financial Aid Factor')),
                ('multiple_residence', models.BooleanField(default=False, help_text=b'Are parents living in separate houses? Check to enable multiple addresses to appear on roster.')),
            ],
            options={
                'ordering': ['famname'],
                'verbose_name_plural': 'Families',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ListExtra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('list', models.SlugField(help_text=b'Should match list name, e.g. &quot;everyone&quot; for everyone@crestmontschool.org.')),
                ('nomail', models.BooleanField(default=False, help_text=b'User can send to list but does not receive mail from it.')),
                ('addresses', models.TextField(help_text=b'Add addresses here, one per line.', blank=True)),
            ],
            options={
                'ordering': ['list'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Obligation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(help_text=b'<strong>Please use the following amounts when entering obligations:</strong><br />       Membership Meeting: 1 unit per meeting<br />        Maintenance/Work Party: Number of hours<br />        Fundraising: Number of hours<br />        Field Trip: Enter 1 unit per trip; partial credits OK e.g. .5 for driving halfway or .25 for BART pickup<br />        Annual Obligation/Scrip: Number of dollars<br />        Housekeeping: Enter 1 unit per cleaning<br />        Committee/Co-op Job: Enter 1 unit per job', max_length=8, choices=[(b'mbsmtg', b'Membership Meeting'), (b'maint', b'Maintenance/Work Party'), (b'fundrais', b'Fundraising'), (b'fldtrp', b'Field Trip'), (b'oblscrp1', b'Annual Obligation/Scrip (1 child enrolled)'), (b'oblscrp2', b'Annual Obligation/Scrip (2 children enrolled)'), (b'housekpg', b'Housekeeping'), (b'cmt_coop', b'Committee/Co-op Job')])),
                ('amount', models.FloatField(help_text=b'Number of units above.')),
                ('note', models.CharField(max_length=255, null=True, blank=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('units', models.CharField(blank=True, max_length=8, null=True, help_text=b'Do NOT select a Unit type when entering a new obligation - this will be auto-filled based on the type of obligation being entered. This field may be edited after saving.', choices=[(b'units', b'Units'), (b'hours', b'Hours'), (b'dollars', b'Dollars')])),
                ('family', models.ForeignKey(to='itaco.Family')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('grad_class', models.CharField(help_text=b'Students expected to graduate at the end of this period are in what grade?', max_length=6, choices=[(b'kind', b'Kindergarten'), (b'1st', b'1st grade'), (b'2nd', b'2nd grade'), (b'3rd', b'3rd grade'), (b'4th', b'4th grade'), (b'5th', b'5th grade'), (b'alum', b'Alumni'), (b'fut', b'Future')])),
                ('current', models.NullBooleanField(help_text=b'Select &quot;Yes&quot; for the current year, &quot;Unknown&quot; for all others. Ignore the &quot;No&quot; option. Only one school year may be marked current at a time.', unique=True)),
            ],
            options={
                'ordering': ['start'],
                'verbose_name_plural': 'School Years',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('birthdate', models.DateField(null=True, blank=True)),
                ('enrolled', models.BooleanField(default=True, help_text=b'Enrolled and Alumni are separate b/c not all students who enroll end up graduating. This way we can keep track of them separately.')),
                ('alumni', models.BooleanField(default=False)),
                ('reader', models.CharField(blank=True, max_length=4, null=True, choices=[(b'morn', b'Morning Reader'), (b'aft', b'Afternoon Reader'), (b'na', b'N/A (Kindergarten)')])),
                ('avatar', easy_thumbnails.fields.ThumbnailerImageField(help_text=b"Please upload an image of your child. Crop the photo in advance so that it's mostly square, not rectangular, and no larger than 600px wide.", upload_to=itaco.models.get_student_avatar_path, null=True, verbose_name=b'Student Photo', blank=True)),
                ('expected_grad_yr', models.ForeignKey(blank=True, to='itaco.SchoolYear', help_text=b'This is an optional field because you may be entering a non-enrolled sibling, who has no grad year. Be sure to select a grad year for enrolled students.', null=True)),
                ('family', models.ForeignKey(to='itaco.Family')),
            ],
            options={
                'verbose_name': 'Student/Sibling',
                'verbose_name_plural': 'Students/Siblings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudentEmergency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('addl_contacts', models.TextField(help_text=b'Add names and phones for additional emergency contacts here, one per line. If none, write "None".', verbose_name=b'Additional Persons Who May Be Called In An Emergency')),
                ('out_of_state_contact', models.TextField(help_text=b'Out of state phone contact (name and phone) in case of earthquake emergency. If none, write "None".', verbose_name=b'Out of State Phone Contact in Case of Earthquake Emergency')),
                ('addl_authorized_take_home', models.TextField(help_text=b'Additional persons authorized to take child home from school (names and phones), one per line. If none, write "None".', verbose_name=b'Additional Persons Authorized to Take Child From School')),
                ('doctor', models.TextField(help_text=b"Name, phone, and insurance info for child's doctor.", verbose_name=b"Child's Doctor")),
                ('dentist', models.TextField(help_text=b"Name, phone, and insurance info for child's dentist.", verbose_name=b"Child's Dentist")),
                ('med_problems', models.TextField(help_text=b'Please list known medical problems. If none, write "None".', verbose_name=b'List of Medical problems')),
                ('allergies', models.TextField(help_text=b'Please list any known medical or food allergies. If none, write "None".')),
                ('auth_tylenol', models.BooleanField(default=False, verbose_name=b'Tylenol')),
                ('auth_polysporin', models.BooleanField(default=False, verbose_name=b'Polysporin (topical antibiotic)')),
                ('auth_antiseptic', models.BooleanField(default=False, verbose_name=b'General Antiseptic')),
                ('auth_benadryl', models.BooleanField(default=False, verbose_name=b'Benedryl (antihistamine)')),
                ('auth_epipen', models.BooleanField(default=False, verbose_name=b'EpiPen (epinephrine)')),
                ('auth_other', models.TextField(help_text=b'If you selected Other above, please describe.', null=True, verbose_name=b'Describe other', blank=True)),
                ('media_release', models.BooleanField(default=True, help_text=b'I authorize the terms of Media Release as described.')),
                ('authorized', models.BooleanField(default=False, help_text=b'This emergency form is not valid until this box is checked and the form is saved.')),
                ('auth_date', models.DateTimeField(auto_now=True)),
                ('student', models.OneToOneField(to='itaco.Student')),
            ],
            options={
                'verbose_name': 'Student Emergency Form',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='credit',
            name='family',
            field=models.ForeignKey(to='itaco.Family'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='charge',
            name='family',
            field=models.ForeignKey(to='itaco.Family'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='billingperiod',
            name='school_year',
            field=models.ForeignKey(to='itaco.SchoolYear'),
            preserve_default=True,
        ),
    ]
