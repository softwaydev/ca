from OpenSSL import crypto

from django import forms
from django.core.exceptions import ObjectDoesNotExist

from ca import models


class RootCrt(forms.ModelForm):

    def save(self, commit=True):
        obj = super().save(commit=False)
        cert_data = obj.crt.read()
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data).get_subject()
        obj.country = cert.C
        obj.state = cert.ST
        obj.location = cert.L
        obj.organization = cert.O
        if cert.OU:
            obj.organizational_unit_name = cert.OU
        if cert.emailAddress:
            obj.email = cert.emailAddress

        if commit:
            obj.save()
        return obj

    def clean(self):
        cleaned_data = super().clean()
        cert_data = cleaned_data.get('crt').read()
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data).get_subject()
        if not cert.C or not cert.ST or not cert.L or not cert.O:
            msg = 'Please enter required field in certificate: Country, State, Location, Organization'
            self.add_error('crt', msg)

    class Meta:
        model = models.RootCrt
        fields = ('key', 'crt')
        labels = {
            'key': 'root .key file',
            'crt': 'root .crt file'
        }


class ConfigRootCrt(forms.Form):
    C = forms.CharField(max_length=2)
    ST = forms.CharField()
    L = forms.CharField()
    O = forms.CharField()
    OU = forms.CharField(required=False)
    CN = forms.CharField()
    emailAddress = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['C'].label = 'Country'
        self.fields['ST'].label = 'State'
        self.fields['L'].label = 'Location'
        self.fields['O'].label = 'Organization'
        self.fields['OU'].label = 'Organizational_unit_name'
        self.fields['CN'].label = 'Common name'
        self.fields['emailAddress'].label = 'Email'


class CreateSiteCrt(forms.Form):
    cn = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cn'].label = 'Common name'

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('cn')
        try:
            models.SiteCrt.objects.get(cn=data)
            msg = "Common name not unique"
            self.add_error('cn', msg)
        except ObjectDoesNotExist:
            pass


class SearchSiteCrt(forms.Form):
    cn = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cn'].label = 'Common name'


class SiteCrt(forms.Form):
    crt_file = forms.FileField(required=False)
    key_file = forms.FileField(required=False)
    crt_text = forms.CharField(widget=forms.Textarea, required=False)
    key_text = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['crt_file'].label = '.crt file'
        self.fields['key_file'].label = '.key file'

    def clean(self):
        cleaned_data = super().clean()
        crt_file = cleaned_data.get('crt_file')
        key_file = cleaned_data.get('key_file')
        crt_text = cleaned_data.get('crt_text')
        key_text = cleaned_data.get('key_text')
        if not ((crt_file and key_file) or (crt_text and key_text)):
            msg = 'Please fill at least 2 fields(files or text)'
            if crt_file or key_file:
                self.add_error('crt_file', msg)
            if crt_text or key_text:
                self.add_error('crt_text', msg)
        if crt_file:
            crt_file_data = crt_file.read()
            crt_file.seek(0)
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, crt_file_data)
            try:
                obj_crt_in_db = models.SiteCrt.objects.get(cn=cert.get_subject().CN)
                if obj_crt_in_db:
                    msg = 'Certificate with Common name already exists in db'
                    self.add_error('crt_file', msg)
            except ObjectDoesNotExist:
                pass
        if crt_text:
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, crt_text)
            try:
                obj_crt_in_db = models.SiteCrt.objects.get(cn=cert.get_subject().CN)
                if obj_crt_in_db:
                    msg = 'Certificate with Common name already exists in db'
                    self.add_error('crt_text', msg)
            except ObjectDoesNotExist:
                pass
        return cleaned_data
