import unittest
from markdown_to_html import to_children, to_paragraph, to_heading, to_code, to_quote, to_unordered_list, to_ordered_list, markdown_to_html_node

class Test_markdown_to_html_node(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_multiple_nodes(self):
        md = """
# This is a heading with _italic_ 

> This is a quote block
> It has **bold** in it

- this is an unordered list
- it has _italic_

1. This is an ordered list
2. It is in plain text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, (
            "<div><h1>This is a heading with <i>italic</i></h1><blockquote>This is a quote block It has <b>bold</b> "
            "in it</blockquote><ul><li>this is an unordered list</li><li>it has <i>italic</i></li></ul><ol><li>This is an ordered list</li><li>It is in plain text</li></ol></div>"),
        )

