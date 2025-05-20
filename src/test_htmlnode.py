import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",)

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        node = ParentNode("", [child_node])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_child(self):
        node = ParentNode("P", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_props(self):
        child_node = LeafNode("c", "This is some text", {"This Key" : "That Value"})
        node = ParentNode("p",[child_node],{"This Key": "That Value"})
        self.assertEqual(node.to_html(),'<p This Key="That Value"><c This Key="That Value">This is some text</c></p>')

    def test_to_html_with_nested_grandchildren(self):
        grandchild_node = LeafNode("b", "spoiled", {"Key" : "Value"})
        grandchild_node2 = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node, grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),'<div><span><b Key="Value">spoiled</b><b>grandchild</b></span></div>')

    def test_to_html_varied_children(self):
        grandchild_node = LeafNode("b", "happy")
        child_node1 = ParentNode("span", [grandchild_node])
        child_node2 = LeafNode("b", "homework", {"Key" : "Value"})
        parent_node = ParentNode("div",[child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), '<div><span><b>happy</b></span><b Key="Value">homework</b></div>')

    def test_multiple_props(self):
        node = ParentNode("div", [LeafNode("span", "hello")], {"class": "container", "id": "main", "data-test": "value"})
        self.assertEqual(node.to_html(), '<div class="container" id="main" data-test="value"><span>hello</span></div>')

    def test_deep_nesting(self):
        great_grandchild = LeafNode("i", "text")
        grandchild = ParentNode("b", [great_grandchild])
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span><b><i>text</i></b></span></div>")

