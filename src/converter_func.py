from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType


"""
tag, value, props
TextType.TEXT: This should return a LeafNode with no tag, just a raw text value.
TextType.BOLD: This should return a LeafNode with a "b" tag and the text
TextType.ITALIC: "i" tag, text
TextType.CODE: "code" tag, text
TextType.LINK: "a" tag, anchor text, and "href" prop
TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
"""


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value =text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value = text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value = text_node.text)
    elif text_node.text_type == TextType.LINK:
        if text_node.url is None:
            raise ValueError("Link text node must have a URL")
        else:
            return LeafNode(tag="a", value= text_node.text, props = {"href" : f"{text_node.url}"})
    elif text_node.text_type == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("Image text node must have a URL")
        else:
            return LeafNode(tag="img", value ="", props = {"src" : f"{text_node.url}", "alt" : f"{text_node.text}"})
    else:
        raise Exception("Text type not recognised")
    

