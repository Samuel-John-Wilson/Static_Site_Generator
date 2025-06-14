from textnode import TextNode, TextType
from blocktype import BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from converter_func import text_node_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from extract_markdown_func import extract_markdown_images, extract_markdown_links
from markdown_to_html import to_children, to_heading, to_paragraph, to_code, to_quote, to_unordered_list, to_unordered_list, markdown_to_html_node
import os
import shutil 

def main():
    node = TextNode("I ate ur dog", TextType.LINK, "http://iateurdog.blogspot.com")
    print(node)

def copy_directory(directory):
    if not os.path.exists(directory):
        raise ValueError("Invalid directory")
    








if __name__=="__main__":
    main()