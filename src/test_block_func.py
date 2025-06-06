import unittest
from blocktype import BlockType
from block_func import markdown_to_blocks, block_to_blocktype

class Test_markdown_to_blocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_null_case(self):
        block = ""
        self.assertEqual(markdown_to_blocks(block), [])

    def test_white_space(self):
        md = """
there was too much whitespace in this string





so we cut it
"""
        output = [
            "there was too much whitespace in this string",
            "so we cut it"
        ]
        self.assertEqual(markdown_to_blocks(md), output)
    

class Test_block_to_blocktype(unittest.TestCase):
    
    def test_ordered_list(self):
        block = """1. ```>-####
2. ```>-####
3. <>
4. --###
5. more string
6. bootsmadethisachallenge
7. keptarguingwithme
8. hewaswrong
9. meatbrainsforthewin
10. ###&><>```"""
        self.assertEqual(block_to_blocktype(block), BlockType.ORDERED_LIST)
        block2 = """ 1. this list is wrong
3. 3 is not 2"""
        self.assertEqual(block_to_blocktype(block2), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = """- this is an unordered list
- these are lines 
- I once stole the declaration of independence
- the one they have now is a fake
- lol
- this text not admissible in court"""
        self.assertEqual(block_to_blocktype(block), BlockType.UNORDERED_LIST)

    def test_quote_block(self):
        block = """> these are the meme arrows
> this is not a green text"""
        self.assertEqual(block_to_blocktype(block), BlockType.QUOTE)

    def test_code_block(self):
        block = "``` this is a code block hurrah```"
        self.assertEqual(block_to_blocktype(block), BlockType.CODE)
    
    def test_heading(self):
        block = "###### this is a heading"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)
    
    def test_half_formatted(self):
        block = "``` this is not a code block"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)
        block2 = """> this is not a quote
> it looks like one though
but it is not"""
        self.assertEqual(block_to_blocktype(block2), BlockType.PARAGRAPH)

    def test_empty(self):
        block = ""
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)
        