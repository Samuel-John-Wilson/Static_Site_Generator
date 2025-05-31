from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType
from extract_markdown_func import extract_markdown_images, extract_markdown_links


"""
tag, value, props
TextType.TEXT: This should return a LeafNode with no tag, just a raw text value.
TextType.BOLD: This should return a LeafNode with a "b" tag and the text
TextType.ITALIC: "i" tag, text
TextType.CODE: "code" tag, text
TextType.LINK: "a" tag, anchor text, and "href" prop
TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
"""


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value =text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value = text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value = text_node.text)
    elif text_node.text_type == TextType.LINK:
        if text_node.url is None:
            raise ValueError("Link text node must have a URL")
        else:
            return LeafNode(tag="a", value= text_node.text, props = {"href" : f"{text_node.url}"})
    elif text_node.text_type == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("Image text node must have a URL")
        else:
            return LeafNode(tag="img", value ="", props = {"src" : f"{text_node.url}", "alt" : f"{text_node.text}"})
    else:
        raise Exception("Text type not recognised")
    




def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise ValueError("invalid markdown, formatted section not closed")
            for i in range(len(split_text)):
                if not split_text[i]:
                    pass
                elif i % 2 == 0:
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes
                    



def split_images(old_nodes):
    
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            continue
        if node.text_type != TextType.TEXT:
            continue
        if not extract_markdown_images(node.text):
            new_nodes.append(node)
        else:
            img = extract_markdown_images(node.text)
            split_text = node.text.split(f"![{img[0][0]}]({img[0][1]})", 1)
            if split_text[0] != "":
                new_nodes.append(TextNode(f"{split_text[0]}", TextType.TEXT))
            if img[0][0] != "":
                new_nodes.append(TextNode(f"{img[0][0]}", TextType.IMAGE, f"{img[0][1]}"))
            while extract_markdown_images(split_text[1]) != []:
                img = extract_markdown_images(split_text[1])
                split_text_again = split_text[1].split(f"![{img[0][0]}]({img[0][1]})", 1)
                if split_text_again[0] != "":
                    new_nodes.append(TextNode(f"{split_text_again[0]}", TextType.TEXT))
                if img[0][0] != "":
                    new_nodes.append(TextNode(f"{img[0][0]}", TextType.IMAGE, f"{img[0][1]}"))
                split_text[1] = split_text_again[1]
            if split_text[1] != "":
                new_nodes.append(TextNode(f"{split_text[1]}", TextType.TEXT))
    return new_nodes
                
           





    




    

