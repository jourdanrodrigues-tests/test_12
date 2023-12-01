from rest_framework import serializers

from app.converters import convert_xml_to_json


class XMLToJSONConverterSerializer(serializers.Serializer):
    file = serializers.FileField(required=True, write_only=True)

    class Meta:
        fields = ['file']


    def validate(self, attrs):
        return convert_xml_to_json(attrs['file'])
