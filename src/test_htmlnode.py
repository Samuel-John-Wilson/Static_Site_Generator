import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("this is a tag", "this is a value", ["this is a list", "boogaloo"])
        node2 = HTMLNode("this is a tag", "this is a value", ["this is a list", "boogaloo"])
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = HTMLNode("this is a tag", "this is a value", ["this is a list", "boogaloo"])
        node2 = HTMLNode()
        self.assertNotEqual(node, node2)
    
    def test_props_to_html(self):
        node = HTMLNode(props= {"thiskey": "thatvalue"})
        call_method = node.props_to_html()
        explicit = [f' {key}="{value}"' for key, value in node.props.items()]
        self.assertEqual(call_method, explicit)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def no_value_err(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def no_tag(self):
        node = LeafNode(None, "this is a value")
        self.assertEqual(node.to_html(), "this is a value")


