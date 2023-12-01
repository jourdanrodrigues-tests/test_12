from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.converters import convert_xml_to_json
from app.serializers import XMLToJSONConverterSerializer


def upload_page(request):
    if request.method == 'GET':
        return render(request, "upload_page.html")
    elif request.method == 'POST':
        file = request.FILES.get('file')
        return JsonResponse(convert_xml_to_json(file))

    return JsonResponse({'error': 'Request method not allowed.'}, status=405)


class ConverterViewSet(GenericViewSet):
    serializer_class = XMLToJSONConverterSerializer
    parser_classes = [MultiPartParser]

    @action(methods=["POST"], detail=False)
    def convert(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
