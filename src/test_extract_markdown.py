import unittest
from extract_markdown_func import extract_markdown_images, extract_markdown_links, extract_title


class Test_extract_markdown_images(unittest.TestCase):
        def test_extract_markdown_images(self):
            matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
            self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
        def test_extract_markdown_multiple_images(self):
            matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) or two ![image](https://i.imgur.com/zjjcJKZ.png)")
            self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        def test_extract_markdown_images_null_case(self):
              matches = extract_markdown_images("there is no image")
              self.assertListEqual([], matches)


class Test_extract_markdown_links(unittest.TestCase):
        def test_extract_markdown_links(self):
               matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
               self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

        def test_extract_markdown_links_null_case(self):
               matches = extract_markdown_links("There is no link")
               self.assertEqual([], matches)

         
class Test_extract_title(unittest.TestCase):
        def test_base_case(self):
            text = """
there is not header on this line
but there will be one soon
# This is a header. Hooray!
## this is a second header! I hope it isn't found.
"""
            output = "This is a header. Hooray!"
            self.assertEqual(extract_title(text), output)
