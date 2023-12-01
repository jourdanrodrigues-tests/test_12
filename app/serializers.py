from rest_framework import serializers

from app.converters import convert_xml_to_json, xml_parsing_error_raise


class XMLToJSONConverterSerializer(serializers.Serializer):
    file = serializers.FileField(required=True, write_only=True)

    class Meta:
        fields = ["file"]

    def validate_file(self, value):
        with xml_parsing_error_raise(serializers.ValidationError("Invalid XML file.")):
            return convert_xml_to_json(value)

    def validate(self, attrs):
        return attrs["file"]
