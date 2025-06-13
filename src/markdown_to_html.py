
from blocktype import BlockType
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


## Quote Block Processing Fix

**Issue**: Quote blocks with multiple lines were rendering without spaces between lines.

**Root Cause**: The original implementation processed each quote line separately using `to_children()`, creating individual HTML nodes for each line. When these nodes rendered, there was no space separator between the content from different lines.

**Solution**: Modified `to_quote()` to first join all quote lines with spaces using `" ".join(quote_lines)`, then process the combined text as a single unit through `to_children()`. This preserves the natural spacing between lines while still allowing inline markdown formatting (bold, italic, etc.) to work correctly within the quote block.

**Example**:
- Before: `"This is a quote blockIt has **bold** in it"`
- After: `"This is a quote block It has **bold** in it"`
"""


def to_children(block):
    block_children = []
    block_text_nodes = text_to_textnodes(block)
    for node in block_text_nodes:
        block_children.append(text_node_to_html_node(node))
    return block_children

# process for Paragraph goes here. / has inline / can child /  <p> tag.
def to_paragraph(block):
    # Replace newlines with spaces and strip extra whitespace - newlines in markdown paragraphs become spaces in html
    normalized_text = block.replace('\n', ' ').strip()
    return ParentNode("p", to_children(normalized_text))

# process for Heading goes here   / has inline / can child / <h1> to <h6> tag, depending on the number of # characters
def to_heading(block):
    split_block = block.split(' ', 1)
    tag = f"h{len(split_block[0])}"
    text = split_block[1] if len(split_block) > 1 else ""
    return ParentNode(tag, to_children(text.strip()))

# process for Code goes here     / no inline / no child / surrounded by <code> tag nested inside a <pre> tag.
def to_code(block):
    block_content = block[3:-3]
    if block_content.startswith('\n'):
        block_content = block_content[1:]
    child = LeafNode("code", block_content)
    return ParentNode("pre", [child])

# process for Quote goes here  <blockquote> tag 
def to_quote(block):
    quote_lines = [] 
    split_block = block.split("\n")
    for line in split_block:
        if not line.strip():
            continue
        new_line = line[2:] # remove '> '
        quote_lines.append(new_line.strip())
    #join all line with spaces, then process as one block
    full_quote_text = " ".join(quote_lines)
    block_children = to_children(full_quote_text)
    return ParentNode("blockquote", block_children)



# process for unordered list goes here  /  <ul> tag, and each list item should be surrounded by a <li> tag.
def to_unordered_list(block):
    block_children = []
    split_block = block.split("\n")
    for line in split_block:
        if not line.strip():
            continue
        new_line = line[2:]
        block_children.append(ParentNode("li", to_children(new_line.strip())))
    
    return ParentNode("ul", block_children)

# process for ordered list goes here  /  <ol> tag, and each list item should be surrounded by a <li> tag
def to_ordered_list(block):
    block_children = []
    split_block = block.split("\n")
    for line in split_block:
        if not line.strip():
            continue
        split_line = line.split('.', 1)
        block_children.append(ParentNode("li", to_children(split_line[1].strip())))
    return ParentNode("ol", block_children)

# This function returns a single parent HTML node with children.
def markdown_to_html_node(markdown):

    # return list of blocks
    children = []
    list_blocks = markdown_to_blocks(markdown)
    for block in list_blocks:
        block_type = block_to_blocktype(block)

        if block_type == BlockType.PARAGRAPH:
            children.append(to_paragraph(block)) 
        elif block_type == BlockType.HEADING:
            children.append(to_heading(block)) 
        elif block_type == BlockType.CODE:
            children.append(to_code(block)) 
        elif block_type == BlockType.QUOTE:
            children.append(to_quote(block)) 
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(to_unordered_list(block)) 
        else:
            children.append(to_ordered_list(block))
    return ParentNode("div", children)

            
             

    