from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    # returns True if ALL of the properties of two TextType objects are the same. 
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    # returns a string representation of the object
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"