import unittest
from htmlnode import LeafNode
from textnode import TextNode, TextType
from converter_func import text_node_to_html_node

"""
tag, value, props | text, text_type, url 
TextType.TEXT: This should return a LeafNode with no tag, just a raw text value.
TextType.BOLD: This should return a LeafNode with a "b" tag and the text
TextType.ITALIC: "i" tag, text
TextType.CODE: "code" tag, text
TextType.LINK: "a" tag, anchor text, and "href" prop
TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
"""



class Test_text_node_to_html_node(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node =  TextNode("This is a link", TextType.LINK, "https://website.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href" : "https://website.com"})

    def test_link_no_url(self):
        node = TextNode("This is a link", TextType.LINK)
        with self.assertRaises(ValueError):        
          html_node = text_node_to_html_node(node)

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "http://test.url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src" : "http://test.url", "alt" : "alt text"})

    def test_image_no_url(self):
        node = TextNode("alt text", TextType.IMAGE)
        with self.assertRaises(ValueError):
            html_node = text_node_to_html_node(node)

    def test_invalid_text_type(self):
    # Create a mock TextNode with an attribute that looks like TextType
    # but isn't one of the expected values
        class MockTextNode:
            def __init__(self, text, text_type):
                self.text = text
                self.text_type = text_type
    
    # Create a node with an invalid text_type
        invalid_node = MockTextNode("Invalid type", "not_a_valid_type")
        with self.assertRaises(Exception):
            html_node = text_node_to_html_node(invalid_node)





    
