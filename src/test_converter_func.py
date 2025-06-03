import unittest
from htmlnode import LeafNode
from textnode import TextNode, TextType
from converter_func import text_node_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link

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




class Test_split_nodes_delimiter(unittest.TestCase):
    def test_base_case(self):
        old_nodes = [TextNode("this has a `code block` in it", TextType.TEXT)]
        output = [TextNode("this has a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" in it", TextType.TEXT)]
        self.assertEqual(output, split_nodes_delimiter(old_nodes, "`", TextType.CODE))

    def test_value_error(self):
        flawed_node = [TextNode("this isn't `closed", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(flawed_node, "`", TextType.CODE)

    def test_not_text_type(self):
        old_nodes = [TextNode("this has a `code block` in it", TextType.TEXT), TextNode("**bold block**", TextType.BOLD)]
        output = [TextNode("this has a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" in it", TextType.TEXT), TextNode("**bold block**", TextType.BOLD)]
        self.assertEqual(output, split_nodes_delimiter(old_nodes, "`", TextType.CODE))

    def test_starts_with_delimiter(self):
        node = [TextNode("`code string` at the start", TextType.TEXT)]
        output = [TextNode("code string", TextType.CODE), TextNode(" at the start", TextType.TEXT)]
        self.assertEqual(output, split_nodes_delimiter(node, "`", TextType.CODE))

    def test_ends_with_delimiter(self):
        node = [TextNode("this ends with `code`", TextType.TEXT)]
        output = [TextNode("this ends with ", TextType.TEXT), TextNode("code", TextType.CODE)]
        self.assertEqual(output, split_nodes_delimiter(node, "`", TextType.CODE))

    def test_multiple_delimiter_pairs(self):
        node = [TextNode("I put some `code` in your `code`, yo dawg", TextType.TEXT)]
        output = [TextNode("I put some ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" in your ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(", yo dawg", TextType.TEXT)]
        self.assertEqual(output, split_nodes_delimiter(node, "`", TextType.CODE))

    def test_adjacent_delimiters(self):
        # double delimiters open-close open-close, so the test in the middle is actually returned as a TEXT node. Double Dilimiters are a mistake. 
        node = [TextNode("``code``", TextType.TEXT)]
        output = [TextNode("code", TextType.TEXT)]
        self.assertEqual(output, split_nodes_delimiter(node, "`", TextType.CODE))

class Test_split_nodes_image(unittest.TestCase):
    def test_null_cases(self):
        plain_text = TextNode("plain text", TextType.TEXT)
        empty_node = TextNode("", TextType.TEXT)
        wrong_type = TextNode("this is code", TextType.CODE)
        not_a_node = "not a node"
        node_no_url = TextNode("![alt]()", TextType.TEXT)
        old_nodes = [plain_text, empty_node, wrong_type, not_a_node, node_no_url]
        output = [TextNode("plain text", TextType.TEXT)]
        self.assertListEqual(split_nodes_image(old_nodes), output)
    
    def test_image_at_front(self):
        node = [TextNode("![alt](http://example.com) the image is at the start of this text", TextType.TEXT)]
        output = [TextNode("alt", TextType.IMAGE, "http://example.com"), TextNode(" the image is at the start of this text", TextType.TEXT)]
        self.assertListEqual(split_nodes_image(node), output)

    def test_image_alone(self):
        node = [TextNode("![alt](http://example.com)", TextType.TEXT)]
        output = [TextNode("alt", TextType.IMAGE, "http://example.com")]
        self.assertListEqual(split_nodes_image(node), output)

    def test_multiple_images(self):
        node = [TextNode("![alt](http://example.com) and another ![alt2](http://second.com)", TextType.TEXT)]
        output = [TextNode("alt", TextType.IMAGE, "http://example.com"), TextNode(" and another ", TextType.TEXT), TextNode("alt2", TextType.IMAGE, "http://second.com")]
        self.assertListEqual(split_nodes_image(node), output)

    def test_multiple_images_no_text(self):
        node = [TextNode("![alt](http://example.com)![alt](http://example.com)", TextType.TEXT)]
        output = [TextNode("alt", TextType.IMAGE, "http://example.com"), TextNode("alt", TextType.IMAGE, "http://example.com")]
        self.assertListEqual(split_nodes_image(node), output)
    
    def test_no_alt(self):
        node = [TextNode("![](www.url.com)", TextType.TEXT)]
        output = [TextNode("", TextType.IMAGE, "www.url.com")]
        self.assertListEqual(split_nodes_image(node), output)

    def test_special_cases(self):
        nodes = [TextNode("![%^/>](url)[alt](url)this is a very long string I wrote for this test case!", TextType.TEXT), TextNode("link", TextType.LINK, "url")]
        output = [TextNode("%^/>", TextType.IMAGE, "url"), TextNode("[alt](url)this is a very long string I wrote for this test case!", TextType.TEXT)]
        self.assertListEqual(split_nodes_image(nodes), output)

class Test_split_nodes_link(unittest.TestCase):
    def test_null_cases(self):
        plain_text = TextNode("plain text", TextType.TEXT)
        empty_node = TextNode("", TextType.TEXT)
        wrong_type = TextNode("this is code", TextType.CODE)
        not_a_node = "not a node"
        node_no_url = TextNode("[link]()", TextType.TEXT)
        old_nodes = [plain_text, empty_node, wrong_type, not_a_node, node_no_url]
        output = [TextNode("plain text", TextType.TEXT)]
        self.assertListEqual(split_nodes_link(old_nodes), output)
    
    def test_link_at_front(self):
        node = [TextNode("[link](http://example.com) the link is at the start of this text", TextType.TEXT)]
        output = [TextNode("link", TextType.LINK, "http://example.com"), TextNode(" the link is at the start of this text", TextType.TEXT)]
        self.assertListEqual(split_nodes_link(node), output)

    def test_link_alone(self):
        node = [TextNode("[link](http://example.com)", TextType.TEXT)]
        output = [TextNode("link", TextType.LINK, "http://example.com")]
        self.assertListEqual(split_nodes_link(node), output)

    def test_multiple_links(self):
        node = [TextNode("[link](http://example.com) and another [link2](http://second.com)", TextType.TEXT)]
        output = [TextNode("link", TextType.LINK, "http://example.com"), TextNode(" and another ", TextType.TEXT), TextNode("link2", TextType.LINK, "http://second.com")]
        self.assertListEqual(split_nodes_link(node), output)

    def test_multiple_links_no_text(self):
        node = [TextNode("[link](http://example.com)[link2](http://example.com)", TextType.TEXT)]
        output = [TextNode("link", TextType.LINK, "http://example.com"), TextNode("link2", TextType.LINK, "http://example.com")]
        self.assertListEqual(split_nodes_link(node), output)
    
    def test_no_alt(self):
        node = [TextNode("[](www.url.com)", TextType.TEXT)]
        output = [TextNode("", TextType.LINK, "www.url.com")]
        self.assertListEqual(split_nodes_link(node), output)
    
    def test_special_cases(self):
        nodes = [TextNode("[%^/>](url)![alt](url)this is a very long string I wrote for this test case!", TextType.TEXT), TextNode("alt", TextType.IMAGE, "url")]
        output = [TextNode("%^/>", TextType.LINK, "url"), TextNode("![alt](url)this is a very long string I wrote for this test case!", TextType.TEXT)]
        self.assertListEqual(split_nodes_link(nodes), output)

 








        

    
