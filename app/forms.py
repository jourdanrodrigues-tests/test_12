from django.core import exceptions
from django.forms import forms

from app.converters import convert_xml_to_json, xml_parsing_error_raise


class UploadFileForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        with xml_parsing_error_raise(exceptions.ValidationError("Invalid XML file.")):
            return convert_xml_to_json(self.cleaned_data["file"])
