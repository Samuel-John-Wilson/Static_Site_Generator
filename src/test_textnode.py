import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.ITALIC, "http://.iateurdog.blogspot.com")
        self.assertNotEqual(node3, node4)

    def test_url_is_none(self):
        node5 = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node5.url)














if __name__ == "__main__":
    unittest.main()
