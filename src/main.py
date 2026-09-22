from copy import copy
import os, shutil, sys

from config import SOURCE, DESTINATION
from textnode import TextNode, TextType
from block_markdown import markdown_to_html_node, extract_title

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
basepath = sys.argv
if len(basepath) == 0:
    basepath = "/"

def main():
    static_to_public()
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
    )

def static_to_public():
    if not os.path.exists(SOURCE):
        raise ValueError("invalid source directory")
    if os.path.exists(DESTINATION):
        print(f"path {DESTINATION} already exists, removing all files inside directory...\n")
        shutil.rmtree(DESTINATION)
    os.mkdir(DESTINATION)
    print(f"copying files from {SOURCE} to {DESTINATION}...\n")
    recursive_copy(SOURCE, DESTINATION)
    print(f"\nfinished, here is what the destination directory looks like:\n{os.listdir(DESTINATION)}")

def recursive_copy(source_path: str, destination_path: str):
    for item in os.listdir(source_path):
        current_path = os.path.join(source_path, item)
        final_path = os.path.join(destination_path, item)
        if os.path.isfile(current_path):
            print(f"current file: {current_path}")
            shutil.copy(current_path, destination_path)
        else:
            print(f"current folder: {current_path}")
            os.mkdir(final_path)
            recursive_copy(current_path, final_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_open = open(from_path, "r+")
    temp_open = open(template_path, "r+")
    markdown_file = from_open.read()
    temp_file = temp_open.read()
    html_file = markdown_to_html_node(markdown_file).to_html()
    html_title = extract_title(markdown_file)
    final_file = temp_file.replace("{{ Title }}", f"{html_title}",)
    final_file = final_file.replace("{{ Content }}", f"{html_file}")
    final_file = final_file.replace('href="/', f'href="{basepath}')
    final_file = final_file.replace('src="/', f'src="{basepath}')
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(final_file)
    to_file.close()
    from_open.close()
    temp_open.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        current_path = os.path.join(dir_path_content, item)
        final_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(current_path) and item.endswith(".md"):
            dest_path = os.path.dirname(dest_dir_path)
            if dest_path != "":
                os.makedirs(dest_path, exist_ok=True)
            generate_page(
                current_path,
                template_path,
                os.path.join(dest_dir_path, item.replace(".md", ".html")),
            )
        elif os.path.isdir(current_path):
            generate_pages_recursive(f"{current_path}",
                template_path, f"{final_path}"
            )





if __name__ == "__main__":
    main()
