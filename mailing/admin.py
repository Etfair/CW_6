from django.contrib import admin

from mailing.models import Mail, Mailing


# Register your models here.


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('name_mail', 'body_mail', 'owner',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('mailing_datetime', 'period', 'mail_status', 'message', 'user',)
