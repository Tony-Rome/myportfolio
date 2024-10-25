import os
from pathlib import Path
import markdown

CONTENT_DIR: str = Path("content")
OUTPUT_DIR: str = Path("output")
STYLES_DIR: str = Path("styles")
CSS_FILE = "styles.css"

OUTPUT_DIR.mkdir(exist_ok=True)


css_source = STYLES_DIR / CSS_FILE
css_target = OUTPUT_DIR / CSS_FILE

if css_source.exists():
    with open(css_source, "r") as f:
        css_content = f.read()
    with open(css_target, "w") as f:
        f.write(css_content)

def convert_md_to_html(md_file):
    html = markdown.markdown(md_file, extensions=["extra", "toc"])
    return html

for root, dirs, files in os.walk(CONTENT_DIR):

    print(f"Root: {files}")

    rel_path = Path(root).relative_to(CONTENT_DIR)
    output_dir: Path = OUTPUT_DIR / rel_path
    output_dir.mkdir(parents=True, exist_ok=True)

    for file in files:
        if file.endswith(".md"):
            md_path = Path(root) / file
            html_filename = file.replace(".md", ".html")
            output_html_path = output_dir / html_filename

            with open(md_path, "r") as f:
                md_content = f.read()

            html_content = convert_md_to_html(md_content)

            html_output = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="/{CSS_FILE}">
                <title>{html_filename}</title>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """

            with open(output_html_path, "w") as f:
                f.write(html_output)

            print(f"Converted {md_path} -> {output_html_path}")
