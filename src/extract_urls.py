import re
from config import IMAGE_URL_PATTERN, REGULAR_URL_PATTERN

def extract_markdown_images(text):
    """
    Extract all instance of ![<image alt>](<url>) markdown from a text

    Args:
        text (str): markdown text to extract

    Returns:
        matches (list): list of tuples containing matching <image alt>, <url pair>
    """
    matches = re.findall(IMAGE_URL_PATTERN, text)
    return matches


def extract_markdown_links(text):
    """
    Extract all instance of [<text alt>](<url>) markdown from a text

    Args:
        text (str): markdown text to extract

    Returns:
        matches (list): list of tuples containing matching <text alt>, <url pair>
    """

    matches = re.findall(REGULAR_URL_PATTERN, text)
    return matches