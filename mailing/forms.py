from django import forms

from mailing.models import Mail, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mail
        exclude = ('owner',)


class MailingForms(forms.ModelForm):

    class Meta:
        model = Mailing
        exclude = ('mail_status', 'user',)
