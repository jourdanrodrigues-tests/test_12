import contextlib
from xml.etree import ElementTree

# As more exception show up from parsing XML, add them here
XML_PARSING_EXCEPTIONS = (ElementTree.ParseError,)

@contextlib.contextmanager
def xml_parsing_error_raise(exception: Exception):
    # Reads "with XML parsing error, raise (e.g.) validation error"
    try:
        yield
    except XML_PARSING_EXCEPTIONS:
        raise exception



def convert_xml_to_json(xml) -> dict:
    # There are many types this "xml "parameter can be, so we're going to trust exception handling to mitigate the lack of types
    def parse_element(element: ElementTree.Element) -> dict:
        # Don't see a value in exposing this function
        if len(element) == 0:
            return {element.tag: element.text or ''}
        return {element.tag: [parse_element(child) for child in element]}

    return parse_element(ElementTree.parse(xml).getroot())
