import wikipedia
import re


def get_wikipedia_text(page_name):
    def clean(text):
        text = re.sub(r"==.*?==+", "", text)
        text = text.replace("\n", "")
        return text

    def remove_parentheses_from_first_sent(text):
        """remove first sentence parentheses as the info contains redundant spelling info"""

    # Specify the title of the Wikipedia page
    wiki = wikipedia.page(page_name)
    # Extract the plain text content of the page
    page_text = wiki.content
    return clean(page_text)
