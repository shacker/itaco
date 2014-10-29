# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models
import accounts.models
import userena.models
from django.conf import settings
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('itaco', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mugshot', easy_thumbnails.fields.ThumbnailerImageField(help_text='A personal image displayed in your profile.', upload_to=userena.models.upload_to_mugshot, verbose_name='mugshot', blank=True)),
                ('privacy', models.CharField(default=b'registered', help_text='Designates who can view your profile.', max_length=15, verbose_name='privacy', choices=[(b'open', 'Open'), (b'registered', 'Registered'), (b'closed', 'Closed')])),
                ('avatar', easy_thumbnails.fields.ThumbnailerImageField(help_text=b'Upload an image of yourself! Please make sure your photo is mostly square, not rectangular.', upload_to=accounts.models.get_avatar_path, null=True, verbose_name=b'Personal Photo / Headshot', blank=True)),
                ('title', models.CharField(help_text=b'e.g. Third Grade Teacher. Right now this is only used for teachers, but could be used for anyone in the future.', max_length=100, blank=True)),
                ('about', models.TextField(help_text=b'Tell us a bit about yourself - interests, work, favorite bands... <br />This field will be displayed on your Profile page.', blank=True)),
                ('tags', models.CharField(help_text=b'Comma-separated keywords. Not displayed on site, but helps your profile get found in site Search.', max_length=255, blank=True)),
                ('email_2', models.EmailField(max_length=75, verbose_name=b'Secondary email', blank=True)),
                ('address1', models.CharField(max_length=100)),
                ('address2', models.CharField(max_length=100, blank=True)),
                ('city', models.CharField(max_length=30)),
                ('state', localflavor.us.models.USStateField(default=b'CA', max_length=2, choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AS', b'American Samoa'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'AA', b'Armed Forces Americas'), (b'AE', b'Armed Forces Europe'), (b'AP', b'Armed Forces Pacific'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'GU', b'Guam'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'MP', b'Northern Mariana Islands'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'PR', b'Puerto Rico'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VI', b'Virgin Islands'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')])),
                ('zip', models.CharField(max_length=10)),
                ('phone_home', localflavor.us.models.PhoneNumberField(max_length=20, blank=True)),
                ('phone_work', localflavor.us.models.PhoneNumberField(max_length=20, blank=True)),
                ('phone_mobile', localflavor.us.models.PhoneNumberField(max_length=20, blank=True)),
                ('fax', localflavor.us.models.PhoneNumberField(max_length=20, blank=True)),
                ('participating_parent', models.BooleanField(default=False, help_text=b'Parent participates in classes. If checked, parent will end up on the participating@ mailing list.')),
                ('no_lists', models.BooleanField(default=False, help_text=b'When checked, this parent will NOT be subscribed to the mailing lists they normally would be.')),
                ('twitter', models.CharField(help_text=b'Your username on Twitter, e.g. &quot;joebob&quot;.', max_length=100, blank=True)),
                ('facebook', models.CharField(help_text=b'Your username on FaceBook, e.g. &quot;janedoe&quot;. <br />Get a FaceBook username <a href=http://www.facebook.com/username/>here</a>.', max_length=100, blank=True)),
                ('url_title', models.CharField(help_text=b'Title of your business or personal URL.', max_length=120, verbose_name=b'URL Title', blank=True)),
                ('url', models.URLField(help_text=b'Business or personal URL.', verbose_name=b'URL', blank=True)),
                ('primary_contact', models.BooleanField(default=False, verbose_name=b'Primary contact for this family?')),
                ('has_timesheet', models.BooleanField(default=False, help_text=b'Enable for staff/faculty who use hourly timesheets (Treasurer will upload via FTP; will become available from members Profile page.)')),
                ('board_pos', models.ManyToManyField(help_text=b'Select the BOARD position(s) this person currently holds.', to='itaco.BoardPosition', verbose_name=b'Board Position', blank=True)),
                ('comm_job', models.ManyToManyField(help_text=b'Select the COMMITTEE JOB(s) (family job) this person currently holds.', to='itaco.CommitteeJob', verbose_name=b'Committee Job', blank=True)),
                ('family', models.ForeignKey(blank=True, to='itaco.Family', null=True)),
                ('list_extras', models.ManyToManyField(help_text=b'Everyone is AUTOMATICALLY added to the lists to which they logically belong. Add ADDITIONAL lists here.', to='itaco.ListExtra', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'permissions': (('view_profile', 'Can view profile'),),
            },
            bases=(models.Model,),
        ),
    ]
