from django.conf.urls.defaults import *
from django.conf import settings
from django.conf.urls.static import static

from itaco.models import *
from itaco.forms import ProfileForm


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Admin, databrowse, filebrowser
    (r'^admin/', include(admin.site.urls)),

    # For django-registration (password resets, etc)
    (r'^accounts/', include('registration.backends.default.urls')),

    # Rosters - family and student listings
    (r'^roster/', include('roster.urls')),

    # Applications - includes public and private URLs (separated for security)
    (r'^apply/', include('apply.urls')),
    (r'^app/', include('apply.private_urls')),

    # Profile editing
    # First match /profiles/edit before django-profiles gets it and loads the defaults, so we can pass in our custom form object.
    # Also we want to support hyphens in URLs to override that one as well.
    (r'^profiles/edit', 'profiles.views.edit_profile', {'form_class': ProfileForm,}),
    url(r'^profiles/(?P<username>[-\w]+)/$', 'profiles.views.profile_detail', name='profiles_profile_detail'),
    (r'^profiles/', include('profiles.urls')),

    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/flower.gif'}),
)


urlpatterns += patterns('itaco.views',

    # Family URLs route to the same view.
    # The family_detail view will then connect to render_to_csv if /csv/ is present.
    # To get data slices we optionally pass in a named year or a named period or the
    # static var "all" (to view all billing periods)

    url(r'^family/(?P<fam_id>\d+)/?$', 'family_detail', name='family_detail'),
    url(r'^family/(?P<fam_id>\d+)/year/(?P<year>\d+)/?$', 'family_detail', name='family_detail_yr'),
    url(r'^family/(?P<fam_id>\d+)/period/(?P<period>\d+)/?$', 'family_detail', name='family_detail_prd'),
    url(r'^family/(?P<fam_id>\d+)/contact/?$', 'family_contact', name='family_contact'),
    url(r'^family/(?P<fam_id>\d+)/all/?$', 'family_detail', {'all':"all"}, name='family_detail_all'),

    # Same views but for CSV. Unfortunately we can't just represent these with a single entry .*(?P<csv>csv)
    # because we'd lose the parameters for specifying the particular billing view.
    url(r'^family/(?P<fam_id>\d+)/(?P<csv>csv)/?$', 'family_detail', name='family_detail_csv'),
    url(r'^family/(?P<fam_id>\d+)/year/(?P<year>\d+)/(?P<csv>csv)/?$', 'family_detail', name='family_detail_csv_yr'),
    url(r'^family/(?P<fam_id>\d+)/period/(?P<period>\d+)/(?P<csv>csv)/?$', 'family_detail', name='family_detail_csv_prd'),
    url(r'^family/(?P<fam_id>\d+)/all/(?P<csv>csv)/?$', 'family_detail', {'all':"all"}, name='family_detail_csv_all'),


    # Misc administrative tools, such as batch daycare charge entry and billing summary
    url(r'^tools/charges/daycare/$', 'batch_charges', {'type':'hrdc'}, name='batch_daycare_charges'),
    url(r'^tools/charges/meal/$', 'batch_charges', {'type':'meal'}, name='batch_meal_charges'),
    url(r'^tools/charges/participation/$', 'batch_participation_credits', name='batch_participation_credits'),
    url(r'^tools/obligations/$', 'batch_obl', name='batch_obl'),
    url(r'^tools/credits/board/$', 'batch_board_credit', name='batch_board_credit'),
    url(r'^tools/credits/board/period/(?P<period>\d+)/$', 'batch_board_credit', name='batch_board_credit_period'),
    url(r'^tools/credits/board/period/(?P<period>\d+)/apply/?$', 'batch_board_credit', {'apply':True}, name='batch_board_credit_apply'),
    url(r'^tools/billing_summary/period/(?P<period>\d+)/?$', 'summary_charges_credits', name='summary_charges_credits'),
    url(r'^tools/billing_summary/$', 'summary_charges_credits', name='summary_charges_credits'),
    url(r'^tools/billing_summary/(?P<csv>csv)/period/(?P<period>\d+)/$', 'summary_charges_credits', name='csv_summary_charges_credits'),
    url(r'^tools/emergency_forms/print/(?P<student_id>\d+)/?$', 'emergency_forms_print', name='emergency_form_detail_print'),
    url(r'^tools/emergency_forms/print/?$', 'emergency_forms_print', name='emergency_forms_all'),
    url(r'^tools/emergency_forms/$', 'emergency_forms', name='emergency_forms'),

    # Edit student info
    url(r'^student/(?P<student_id>\d+)/edit/?$', 'edit_student', name='edit_student'),
    url(r'^student/(?P<student_id>\d+)/emergency/edit/?$', 'edit_student_emergency', name='edit_student_emergency'),

    # Administrator's view of all obligations owed on one page
    url(r'^tools/obligation_summary/year/(?P<year>\d+)$', 'obligation_summary', name='obligation_summary'),

    # Generate mailing list members
    url(r'^lists/$', 'listgen', name='listgen'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



if settings.DEBUG:
    urlpatterns += patterns('',

      (
          r'^media[/]+(?P<path>.*)$',
          'django.views.static.serve',
          {'document_root': settings.MEDIA_ROOT}
      ),

    )
