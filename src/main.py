from textnode import TextNode, TextType
from blocktype import BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from converter_func import text_node_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from extract_markdown_func import extract_markdown_images, extract_markdown_links, extract_markdown_header
from markdown_to_html import to_children, to_heading, to_paragraph, to_code, to_quote, to_unordered_list, to_unordered_list, markdown_to_html_node
import os
import shutil 

dir_log =[]


def clear_dl():
    global dir_log
    dir_log = []

def copy_directory(src, destination):
    global dir_log
    if not os.path.exists(src):
        raise ValueError("Invalid source directory")
    # delete directory, then recreate it empty
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.makedirs(destination)
    src_list = os.listdir(src)
    for item in src_list:
        file_path = os.path.join(src, item)
        dest_path = os.path.join(destination, item)

        if os.path.isfile(file_path):
            dir_log.append(file_path)
            shutil.copy(file_path, dest_path)
        elif os.path.isdir(file_path):
            dir_log.append(file_path)
            copy_directory(file_path, dest_path)
        else:
            dir_log.append(f"{file_path} object was neither file nor directory")
    print(dir_log)


    
    




def main():
    clear_dl()
    copy_directory("./static", "./public")
    

if __name__=="__main__":
    main()