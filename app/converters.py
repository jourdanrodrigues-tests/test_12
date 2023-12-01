from xml.etree import ElementTree


def convert_xml_to_json(xml) -> dict:
    # There are many types this "xml "parameter can be, so we're going to trust exception handling to mitigate the lack of types
    def parse_element(element: ElementTree.Element) -> dict:
        # Don't see a value in exposing this function
        if len(element) == 0:
            return {element.tag: element.text or ''}
        return {element.tag: [parse_element(child) for child in element]}

    return parse_element(ElementTree.parse(xml).getroot())
