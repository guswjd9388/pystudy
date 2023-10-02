import re


def remove_xml_tag(text: str) -> str:
    return re.sub(r'\<\?xml[^\?].+\?\>', '', text)
