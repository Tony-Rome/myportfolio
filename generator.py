import os
import re
from pathlib import Path
from typing import AnyStr

import markdown
from myportfolio.contants import CONTENT_DIR_NAME, OUTPUT_DIR_NAME, STYLES_DIR_NAME, STYLES_FILE_NAME, MENU_FILE_NAME

content_path: Path = Path(f"../{CONTENT_DIR_NAME}")
output_path: Path = Path(f"../{OUTPUT_DIR_NAME}")
styles_path: Path = Path(f"../{STYLES_DIR_NAME}")
menu_path: Path = content_path / MENU_FILE_NAME

css_source_path = Path(f"../{STYLES_DIR_NAME}/{STYLES_FILE_NAME}")
css_target_path = Path(f"../{OUTPUT_DIR_NAME}/{STYLES_FILE_NAME}")

output_path.mkdir(exist_ok=True)

def create_css_file():
    if css_source_path.exists():
        css_file = write_or_read_file(path=css_source_path)
        write_or_read_file(path=css_target_path, file=css_file, action=False)


def convert_md_to_html(md_file):
    html = markdown.markdown(md_file, extensions=["extra", "toc", "fenced_code", "codehilite"], tab_length=2)
    return html

def get_content_menu_html():
    if menu_path.exists():
        menu_content = write_or_read_file(path=menu_path)
        return convert_md_to_html(menu_content)
    else:
        return ""

def write_menu_html(menu_html):
    menu_output_path = f"{output_path}/{MENU_FILE_NAME}"
    menu_output_path = menu_output_path.replace(".md", ".html")
    write_or_read_file(path=menu_output_path, file=menu_html, action=False)

def generate_html_content(html_file_name, html_content, menu_content, styles_path):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="{styles_path}{STYLES_FILE_NAME}">
        <title>{html_file_name}</title>
    </head>
    <body>
        <div class="base-line"></div>
        <div class="container">
            <div class="menu">{menu_content}</div>
            <div class="content">{html_content}</div>
            <div class="contact">Contacts
                <div class=container-contact>
                    <a href="https://github.com/Tony-Rome">
                        <img src="https://cdn-icons-png.flaticon.com/512/2111/2111432.png" alt="Github" />
                    </a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

def write_or_read_file(path, file=None, action=True) -> AnyStr:
    if action:
        with open(path, "r") as f:
            return f.read()
    else:
        with open(path, "w") as f:
            f.write(file)
            return ""

def create_relative_base_path(path):
    path = re.sub(r'\.', '', str(path))
    path = re.sub(r'\w+', '../', str(path))
    path = re.sub(r'\\', '', path)
    return './' + path

def create_content():

    create_css_file()

    menu_content = get_content_menu_html()
    write_menu_html(menu_html=menu_content)

    for root, dirs, files in os.walk(content_path):
        rel_path = Path(root).relative_to(content_path)
        output_dir: Path = Path(f"{output_path}/{rel_path}")
        output_dir.mkdir(parents=True, exist_ok=True)

        styles_path = create_relative_base_path(path=rel_path)

        for file in files:

            if file == MENU_FILE_NAME:
                continue

            md_path = Path(root) / file
            html_file_name = file.replace(".md", ".html")
            output_html_path = output_dir / html_file_name

            md_content = write_or_read_file(path=md_path)

            html_content = convert_md_to_html(md_content)

            html_output = generate_html_content(html_file_name=html_file_name, html_content=html_content,
                                                menu_content=menu_content, styles_path=styles_path)

            write_or_read_file(path=output_html_path, file=html_output, action=False)


create_content()