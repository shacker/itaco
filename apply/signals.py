from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from itaco.models import BoardPosition

def app_submitted(sender, instance, signal, created, **kwargs):
    """When an app is submitted, alert admissions people as well as submittor (with separate messages). """

    # We'll need this in the email template
    enrollment_chairs = BoardPosition.objects.get(title='Admissions').profile_set.all()

    # Ensure we don't re-send email every time app is updated.
    if created:

        # To avoid circular dependencies, import needs to be inside the signal, not at the top
        from apply.models import Application
        app = Application.objects.get(pk=instance.id)
        site = Site.objects.get(id=1) # Need this for link in email template.

        # Send email to site admins
        recipients = ['admissions@crestmontschool.org',]
        email_subject = render_to_string("apply/admin-newapp-subject.txt", { 'app': app })
        email_body_txt = render_to_string("apply/admin-newapp-body.txt", { 'app': app, 'site': site, })
        msg = EmailMessage(email_subject, email_body_txt, "Crestmont Admissions <info@crestmontschool.org>", recipients)
        msg.send(fail_silently=False)

        # Send email to applying parents
        recipients = [app.par1_email,app.par2_email]
        email_subject = 'Thanks for applying to Crestmont'
        email_body_txt = render_to_string("apply/appl-newapp-body.txt", { 'app': app, 'site': site, 'enrollment_chairs': enrollment_chairs,})
        msg = EmailMessage(email_subject, email_body_txt, "Crestmont Admissions <admissions@crestmontschool.org>", recipients)
        msg.send(fail_silently=False)


