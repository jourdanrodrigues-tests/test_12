from collections import defaultdict

from django.http import JsonResponse
from django.shortcuts import render
from xml.etree import ElementTree


def upload_page(request):
    if request.method == 'GET':
        return render(request, "upload_page.html")
    elif request.method == 'POST':
        tree = ElementTree.parse(request.data['file'])
        return JsonResponse(parse_element(tree.getroot()))

    return JsonResponse({'error': 'Request method not allowed.'}, status=405)


def parse_element(element: ElementTree.Element) -> dict:
    output = defaultdict(list)
    for child in element:
        output[child.tag].append(parse_element(child))
    return output

