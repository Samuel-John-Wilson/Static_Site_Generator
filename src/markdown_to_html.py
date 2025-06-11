
from blocktype import blocktype
from block_func import markdown_to_blocks, block_to_blocktype
from converter_func import text_node_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType



"""Assignment
Create a new function called def markdown_to_html_node(markdown): that converts a full markdown document into a single parent HTMLNode.
That one parent HTMLNode should (obviously) contain many child HTMLNode objects representing the nested elements.

FYI: I created an additional 8 helper functions to keep my code neat and easy to understand, because there's a lot of logic necessary for markdown_to_html_node.
 I don't want to give you my exact functions because I want you to do this from scratch. However, I'll give you the basic order of operations:

Split the markdown into blocks (you already have a function for this)
Loop over each block:
Determine the type of block (you already have a function for this)
Based on the type of block, create a new HTMLNode with the proper data
Assign the proper child HTMLNode objects to the block node.
 I created a shared text_to_children(text) function that works for all block types. 
 It takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions (think TextNode -> HTMLNode).
The "code" block is a bit of a special case: it should not do any inline markdown parsing of its children. 
I didn't use my text_to_children function for this block type, I manually made a TextNode and used text_node_to_html_node.
Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.

"""



    

def markdown_to_html_node(markdown):

    # return list of blocks
    list_blocks = markdown_to_blocks(markdown)
    for block in list_blocks:
        block_type = block_to_blocktype(block)

        if block_type == BlockType.PARAGRAPH:
            pass # process for Paragraph goes here. / has inline / can child /  <p> tag.
        elif block_type == BlockType.HEADING:
            pass # process for Heading goes here   / has inline / can child / <h1> to <h6> tag, depending on the number of # characters
        elif block_type == BlockType.CODE:
            pass # process for Code goes here     / no inline / no child / surrounded by <code> tag nested inside a <pre> tag.
        elif block_type == BlockType.QUOTE:
            pass # process for Quote goes here   / no inline / no child /  <blockquote> tag 
        elif block_type == BlockType.UNORDERED_LIST:
            pass # process for unordered list goes here  /  <ul> tag, and each list item should be surrounded by a <li> tag.
        else:
            pass # process for ordered list goes here  /  <ol> tag, and each list item should be surrounded by a <li> tag.

            # Write out the methods for each type. Might go in block_func? 
            # This function returns a single parent HTML node with children. 

    