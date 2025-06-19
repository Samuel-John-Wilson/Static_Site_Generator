from textnode import TextNode, TextType
from blocktype import BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from converter_func import text_node_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from extract_markdown_func import extract_markdown_images, extract_markdown_links, extract_title
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


    
def generate_page(from_path, template_path, dest_path):
    # check that paths exist 
    if not os.path.exists(from_path):
        raise ValueError("source path invalid")
    if not os.path.exists(template_path):
        raise ValueError("template path invalid")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    print(f"Generating page {from_path} to {dest_path} using {template_path}")
    # read the template and content files and save them as variables
    with open(from_path, 'r', encoding='utf-8') as source:
        content = source.read()
    with open(template_path, 'r', encoding='utf-8') as temp:
        template = temp.read()
    if not content:
        raise ValueError("source file empty")
    if not template:
        raise ValueError("template file empty")
    # extract title, turn markup content into html
    html_content = markdown_to_html_node(content).to_html() 
    title = extract_title(content)
    # Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated
    final_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    #write final html file
    with open(dest_path, 'w', encoding='utf-8') as output_file:
        output_file.write(final_page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    global dir_log
    if not os.path.isdir(dir_path_content):
        raise ValueError("Content path invalid")
    list_content = os.listdir(dir_path_content)
    for item in list_content:
        item_path = os.path.join(dir_path_content, item)
        item_dest = os.path.join(dest_dir_path, item)
        if os.path.isdir(item_path):
            new_dest = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, new_dest)
        elif os.path.isfile(item_path) and item_path.endswith(".md"):
            html_item_dest = os.path.splitext(item_dest)[0] + ".html"
            generate_page(item_path, template_path, html_item_dest)
        else:
            dir_log.append(f"unknown file at {item_path} not processed")




def main():
    clear_dl()
    copy_directory("./static", "./public")
    generate_pages_recursive("./content", "./template.html", "./public")
    

if __name__=="__main__":
    main()