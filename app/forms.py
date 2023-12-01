from django.forms import forms

from app.converters import xml_parse_error_raise, convert_xml_to_json


class UploadFileForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        with xml_parse_error_raise(forms.ValidationError('Invalid XML file.')):
            return convert_xml_to_json(self.cleaned_data["file"])
