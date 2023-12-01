from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.forms import UploadFileForm
from app.serializers import XMLToJSONConverterSerializer


def upload_page(request):
    if request.method not in ['POST', 'GET']:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            return JsonResponse(form.cleaned_data['file'])
    else:
        form = UploadFileForm()

    return render(request, "upload_page.html", {"form": form})


class ConverterViewSet(GenericViewSet):
    serializer_class = XMLToJSONConverterSerializer
    parser_classes = [MultiPartParser]

    @action(methods=["POST"], detail=False)
    def convert(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
