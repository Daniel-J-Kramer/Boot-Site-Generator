from textnode import TextNode, TextType
from htmlnode import HTMLNode
from blocks import BlockType, markdown_to_html_node
import shutil
import os
import sys
def main():
    if sys.argv[0]:
        basepath = sys.argv[0]
    else:
        basepath = "/"
    target_dir = f".{basepath}docs"
    source_dir = f".{basepath}static"
    content_dir = f".{basepath}content"
    template = f".{basepath}template.html"
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.mkdir(target_dir)
    copy_static(source_dir, target_dir)
    generate_pages_recursive(content_dir, template, target_dir, basepath)

def copy_static(source_dir: str, target_dir: str):
    dir_contents = os.listdir(source_dir)

    for content in dir_contents:
        if os.path.isfile(f"{source_dir}/{content}"):
            shutil.copy(f"{source_dir}/{content}", target_dir)
        elif os.path.isdir(f"{source_dir}/{content}"):
            os.mkdir(f"{target_dir}/{content}")
            copy_static(f"{source_dir}/{content}", f"{target_dir}/{content}")

def extract_title(markdown):
    opened_file = open(markdown)
    read_file = opened_file.read()
    split_lines = read_file.split("\n\n")
    opened_file.close()
    for line in split_lines:
        if line.startswith("# "):
            final_line = line[2:]
            return final_line
    
    raise Exception("No h1 header found")
    

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    source = open(from_path)
    template = open(template_path)
    read_markdown = source.read()
    read_temp = template.read()
    source.close()
    template.close()

    contents = markdown_to_html_node(read_markdown).to_html()
    title = extract_title(from_path)
    read_temp = read_temp.replace("{{ Title }}", title)
    read_temp = read_temp.replace("{{ Content }}", contents)
    read_temp = read_temp.replace("href=\"/", f"href=\"{basepath}")
    read_temp = read_temp.replace("src=\"/", f"src=\"{basepath}")

    destination = open(dest_path, "w")
    destination.write(read_temp)
    destination.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_contents = os.listdir(dir_path_content)

    for content in dir_contents:
        if os.path.isfile(f"{dir_path_content}/{content}") and str(content).endswith("md"):
            generate_page(f"{dir_path_content}/{content}", template_path, f"{dest_dir_path}/index.html", basepath)
        elif os.path.isdir(f"{dir_path_content}/{content}"):
            os.mkdir(f"{dest_dir_path}/{content}")
            generate_pages_recursive(f"{dir_path_content}/{content}", template_path, f"{dest_dir_path}/{content}", basepath)

main()