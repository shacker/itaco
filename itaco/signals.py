def update_profile(sender, instance, signal, created, **kwargs):
    """When profile is updated, generate mail to webmaster."""

    from models import Profile
    from django.contrib.sites.models import Site
    from django.template.loader import render_to_string
    from django.core.mail import EmailMessage

    profile = Profile.objects.get(pk=instance.id)
    site = Site.objects.get(id=1) # Need this for link in email template. Jschool's site ID in settings is 1.

    recipients = ['shacker@birdhouse.org',]
    email_subject = render_to_string("tools/profiles/profile_update-subject.txt", { 'p': profile })
    email_body_txt = render_to_string("tools/profiles/profile_update-body.txt", { 'p': profile, 'site': site, })

    msg = EmailMessage(email_subject, email_body_txt, "shacker@birdhouse.org", recipients)
    msg.send(fail_silently=False)




